# Congressional Grade Level Plotting
# Mark Delcambre
# 
#


# Import the necessary libraries.
# RgoogleMaps is imported for the plotting of the map on google maps
# RColorBrewer is used for the coloring of the heat map.
library(RgoogleMaps)
library(RColorBrewer)
library(scales)


# Download the relevant Sunlight CongressionalPublic Data into the data directory
if(!file.exists("data")){
    dir.create("data")
}
file_url <- "https://data.sunlightlabs.com/api/views/iwhe-qaqu/rows.csv?accessType=DOWNLOAD"
file_loc <- "./data/Members_And_Grade_Level.csv"
if(!file.exists(file_loc)){
    download.file(file_url,destfile=file_loc,method="curl")
    cat("## Date Downloaded", as.character(Sys.Date()),'\n',file=file_loc,append=T)
}

# Setup the output folder for the images we are plotting
if(!file.exists("output")){
    dir.create("output")
}

# Read the file into memory, last I checked this file is about 200 MB. May need to start subsampling
# Then remove the NA columns for lat lon.
#data <- read.csv(file=file_loc, header=T, comment.char="#")
