#!/bin/sh

# shell script to download PRISM data with FTP

echo "Enter your email: "
read pass

echo

echo "Enter the years you want to download seperated with a space (ex: '2000 2001 2002'): "
read years

echo

# create daily-data folder
if [ ! -d ./daily-data ]
then
    mkdir daily-data
fi

# download files
for year in $years;
do
    echo "---- Starting download for year $year ----"
    echo

    wget --quiet --show-progress --no-clobber --directory-prefix ./daily-data --ftp-user=anonymous --ftp-password=$pass ftp://prism.nacse.org/daily/tmean/2019/*

    echo
    echo "---- $year files are done downloading ----"
done


echo && echo


# extract zip files
echo "Would you like to extract all the files (y/n):"
read extract

echo

if [ $extract == "y" ]
then
    cd daily-data/

    echo "---- Starting file extraction ----"
    echo

    for z in $( ls | grep .zip );
    do

        # get the file name withouth the .zip
        name=$(echo $z | awk '{print substr($0, 0, length($0)-4)}')
        echo $name

        mkdir $name
        unzip $z -d $name

    done

    echo
    echo "---- Done extracting all files ----"
else
    echo "Quiting Program"
    exit
fi


echo && echo


# deleting the zip files
echo "Would you like to delete the zip files (y/n):"
read delete

echo

if [ $delete == "y" ]
then
    echo "---- Starting zip deletion ----"
    echo

    rm *.zip

    echo
    echo "---- Zip deletion done ----"
else
    echo "Quiting Program"
    exit
fi
