#!/bin/bash

popt=false
fopt=false
hopt=false
dopt=false
NAME=""
FILE_PATH=""
DELAY=""
VERIFY=""
PROFILE="default"

set -e

###################################################################
# Help                                                            #
###################################################################

Help()
{
    # Display Help
    echo "This utility will create, update, and fetch secrets from AWS Secrets Manager,"
    echo "using the default profile or the named profile provided. This tools only"
    echo "accepts files as input for the secret values."
    echo
    echo "usage: secrets.sh [ -p | --put | -f | --fetch | -d | --delete]"
    echo "       [ -h | --help ] [ --name ] [ --path ] [ --profile ]"
    echo "options:"
    echo "  -h | --help     Displays this information"
    echo
    echo "create/update:"
    echo "  -p | --put      Will create a new secret or update a pre-exisitng"
    echo "  --name          The name of the affected secret."
    echo "  --path          The path to .json file containing secret key:value pairs."
    echo "  --profile       The AWS profile to be used."
    echo
    echo "fetch:"
    echo "  -f | --fetch    Fetches and prints a secret's latest version."
    echo "  --name          The name of the affected secret."
    echo "  --profile       The AWS profile to be used."
    echo
    echo "delete:"
    echo "  -d | --delete   Deletes an existing secret after specified delay."
    echo "  --name          The name of the affected secret."
    echo "  --delay         Number of days to wait before deletion."
    echo "  --profile       The AWS profile to be used."
    echo
}

###################################################################
# PutSecret                                                       #
###################################################################

PutSecret()
{
    if [ -z "$NAME" ]
    then
        read -p "Enter Secret Name: " NAME
    fi
    if [ -z "$FILE_PATH" ]
    then
        read -p "Enter Path to Secrets File: " FILE_PATH
    fi

    if result=$(aws secretsmanager create-secret --name $NAME --secret-string "file://${FILE_PATH}" --profile $PROFILE 2> /dev/null)  ; then
        echo "New Secret Created: ${result}"
    else
        result=$(aws secretsmanager put-secret-value --secret-id $NAME --secret-string "file://${FILE_PATH}" --profile $PROFILE 2> /dev/null)
        echo "Secret ${NAME} updated: ${result}"
    fi
}

###################################################################
# FetchSecret                                                     #
###################################################################

FetchSecret()
{
    if [ -z "$NAME" ]
    then
        read -p "Enter Secret Name: " NAME
    fi

    aws secretsmanager get-secret-value --secret-id $NAME --profile $PROFILE
}

###################################################################
# FetchSecret                                                     #
###################################################################

DeleteSecret()
{
    if [ -z "$NAME" ]
    then
        read -p "Enter Secret Name: " NAME
    fi

    if [ -z "$DELAY" ]
    then
        read -p "Enter Deletion Delay (days): "
    fi

    if [ -z "$DELAY" ] || [ "$DELAY" -eq "0" ]
    then
        read -p "This will immediately delete the secret with no recovery options, is this acceptable? [y/n]: " VERIFY
        if [[ ! "$VERIFY" =~ ^[Yy]$ ]]
        then
            echo "Verification denied, exiting.."
            exit 0
        fi
        aws secretsmanager delete-secret --secret-id $NAME --force-delete-without-recovery --profile $PROFILE
    else
        aws secretsmanager delete-secret --secret-id $NAME --recovery-window-in-days $DELAY --profile $PROFILE
    fi

}

###################################################################
# Main                                                            #
###################################################################

while [[ $# -gt 0 ]]; do
    opt="$1"
    case "$opt" in
        "-h" | "--help"     )   hopt=true; shift;;
        "-f" | "--fetch"    )   fopt=true; shift;;
        "-p" | "--put"      )   popt=true; shift;;
        "-d" | "--delete"   )   dopt=true; shift;;
        "--name"            )   NAME="$2"; shift; shift;;
        "--path"            )   FILE_PATH="$2"; shift; shift;;
        "--delay"           )   DELAY="$2"; shift; shift;;
        "--profile"         )   PROFILE="$2"; shift; shift ;;
        *                   )   echo "ERROR: Invalid option: \""$opt"\"" >&2
                            exit 1;;
    esac
done



if $hopt && ! $popt && ! $fopt && ! $dopt
    then
    Help
    exit 1
fi

if ! $hopt && $popt && ! $fopt && ! $dopt
    then
    PutSecret
    exit 1
fi

if ! $hopt && ! $popt && $fopt && ! $dopt
    then
    FetchSecret
    exit 1
fi

if ! $hopt && ! $popt && ! $fopt && $dopt
    then
    DeleteSecret
    exit 1
fi

if ! $hopt && ! $popt && ! $fopt && ! $dopt
    then
        echo "ERROR: Missing Required Option: -h or --help for usage information."
        exit 1
fi

