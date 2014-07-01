# Congress Retention rate - Map
# Mark Delcambre
# 
#
# Shape file acquired from ArcGIS
# http://www.arcgis.com/home/item.html?id=a5e84bcbbd9b44688d20a1a48e03723d


# Import the necessary libraries.
# RgoogleMaps is imported for the plotting of the map on google maps
# RColorBrewer is used for the coloring of the heat map.
library(RColorBrewer)
library(maptools)
library(scales)
library(maps)
library(classInt)

data(state.fips)


# Download the relevant Seattle Public Data into the data directory
if(!file.exists("data")){
    dir.create("data")
}
file_url <- "https://raw.githubusercontent.com/sunlightlabs/eff_scorecard/master/scores.csv"
file_loc <- "./data/nsa_scorecard.csv"
if(!file.exists(file_loc)){
    download.file(file_url,destfile=file_loc,method="curl")
    cat("## Date Downloaded", as.character(Sys.Date()),'\n',file=file_loc,append=T)
}

# The shape file was downloaded from the census website at the following link and placed in the data directory (created below)
# The retention data we have is from the 111th congress, so make sure to download the correct shapefile.
# https://www.census.gov/cgi-bin/geo/shapefiles2010/layers.cgi
# Zip file is unzipped into a folder named 'dist'
polys <- readShapeSpatial("dist/tl_2010_us_cd111.shp")



# Setup the output folder for the images we are plotting
if(!file.exists("output")){
    dir.create("output")
}

# Read the file into memory, last I checked this file is about 200 MB. May need to start subsampling
# Read the csv file into memory, and remove nulls and senetors.
dframe <- read.csv(file=file_loc, header=T, comment.char="#", na.strings = "?", skipNul=T, stringsAsFactors=F)
dframe <- dframe[complete.cases(dframe$grade,dframe$district),] 

# Add a column for FIPS code-district and then match the grade into the ploys dataframe.
dframe[["st_district"]] <- paste(state.fips[match(dframe[["state"]],state.fips$abb),"fips"],dframe[["district"]], sep="-")
polys$ret_rate <- dframe[match(paste(as.numeric(polys$STATEFP10),as.numeric(polys$CD111FP),sep="-"),dframe$st_district),"grade"]

# colors<-rev(brewer.pal(5,"RdYlGn")) # Not colorblind friendly
colors <- rev(c('#ffffcc','#c2e699','#78c679', '#31a354', '#006837')) # Green -> Yellow Color blind friendly

png("output/NSA_Grade.png")

# Plot the map using the colors, limiting to lover 48
plot(polys,group=polys$grade,col=colors,xlim=c(-125,-65.5),ylim=c(24.2,49.7))

dev.off()
