def add_submission(observables=None, mode=None, **kwargs):
    # create a new submission object with root analysis
    submission = Submission(root_analysis=Analysis(), **kwargs)

    # include root analysis in list of submission analysis
    submission.analysis.append(submission.root_analysis)

    # add mode to submission modes
    if mode:
        mode = create(Mode, name=mode)
        submission.modes.append(mode)

    # insert and refresh the submission object
    db.session.add(submission)
    db.session.commit()
    db.session.refresh(submission)

    # update the root analysis with the observables
    update_analysis(id=submission.root_analysis.id, observables=observables)

def update_analysis(id=None, target=None, observables=None, **kwargs):
    # find the analysis
    analysis = db.session.query(Analysis).filter(Analysis.id == id).one()

    # update the target observable metadata
    if target:
        add_observable(analysis, **target)

    # add child observables
    for observable in observables or []:
        observable = add_observable(analysis, **observable)
        analysis.observables.append(observable)

    # update analysis attributes
    for attr, value in kwargs.items():
        setattr(analysis, attr, value)
    db.session.commit()

    # queue all new analysis
    queue_analysis(analysis)

def add_observable(analysis, metadata=None, **kwargs):
    # create the observable
    observable = create(Observable, **kwargs)

    # create observable metadata and map it to the observable via analysis
    for m in metadata:
        m = create(Metadata, **m)
        m = create(ObservableMetadata, observable=observable, metadata=m)
        analysis.observable_metadata.append(m)

    return observable

def queue_analysis(analysis):
    # get list of submissions that contain the analysis
    query = db.session.query(Submission).join(SubmissionAnalysis).filter(SubmissionAnalysis.analysis_id == analysis.id)
    submissions = query.all()

    # queue the target observable from the analysis in case we added new directives
    if analysis.target:
        queue_observable(submission, analysis, analysis.target)

    # queue each child observable
    for observable in analysis.observables:
        queue_observable(submission, analysis, observable)

def queue_observable(submission, analysis, observable):
    # get the directives for the observable from the analysis
    observable_directives = []
    for observable_metadata in analysis.observable_metadata:
        if observable_metadata.observable.id == observable.id and observable_metadata.metadata.type == 'directive':
            observable_directives.append(observable_metadata.metadata.value)

    # for every module in the submission modes
    for mode in submission.mode:
        for module in mode.modules:

            # skip module if observable is not a valid type
            if observable.type not in module.observable_types.split(',')
                continue

            # skip module if observable does not have the required directive
            if module.required_directive and module.required_directive not in observable_directives:
                continue

            # add module analysis to submission
            module_analysis, created = _create(Analysis, type=module.name, target=observable.id)
            submission.analysis.append(module_analysis)
            db.session.commit()

            # if we just created the module analysis then add it to sqs queue
            if created:
                queue(module_analysis) 

            # if the module analysis already existed
            else:
                # TODO: prevent infinite loop somehow
                queue_analysis(module_analysis)

def create(cls, **kwargs):
    instance, created = _create(cls, **kwargs)
    return instance

def _create(cls, **kwargs):
    # try inserting the thing
    try:
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        db.session.refresh(instance)
        return instance, True

    # if it already is in the database then return the existing copy
    except IntegrityError:
        db.session.rollback()
        return db.session.query(cls).filter_by(**kwargs).one(), False
