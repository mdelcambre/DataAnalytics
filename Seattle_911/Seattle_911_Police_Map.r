# Seattle Public Data Heatmap
# Mark Delcambre
# 
#
# Code significantly based on Myles Harrison Toronto Camera Heat Map
# http://www.everydayanalytics.ca


# Import the necessary libraries.
# MASS is imported for the 2d kde for the heatmap
# RgoogleMaps is imported for the plotting of the map on google maps
# RColorBrewer is used for the coloring of the heat map.
library(MASS)
library(RgoogleMaps)
library(RColorBrewer)
library(scales)


# Download the relevant Seattle Public Data into the data directory
if(!file.exists("data")){
    dir.create("data")
}
file_url <- "https://data.seattle.gov/api/views/3k2p-39jp/rows.csv?accessType=DOWNLOAD"
file_loc <- "./data/seattle_911_police_response.csv"
if(!file.exists(file_loc)){
    download.file(file_location,destfile=file_loc,method="curl")
    cat("## Date Downloaded", as.character(Sys.Date()),'\n',file=file_loc,append=T)
}

# Read the file into memory, last I checked this file is about 200 MB. May need to start subsampling
# Then remove the NA columns for lat lon.
data <- read.csv(file=file_loc, header=T, comment.char="#")
data <- data[complete.cases(data["Latitude"],data["Longitude"]),]
# data <- data[data["Latitude"] > 47.5545 & data["Latitude"]<47.69270 & data["Longitude"] > -122.4376 & data["Longitude"] < -122.2216,]

# Center for the Google Map
center <- sapply(c(data["Latitude"],data["Longitude"]),mean)


# Setup Colors from Green to Red.
# Add transparency
colors <- rev(colorRampPalette(brewer.pal(11, 'RdYlGn'))(500))
colors_a <-alpha(colors,0.5)



# Loop through each of the crime categories. Create a heatmap for each one and save them as a new png file.
for (crime in levels(data[["Event.Clearance.Group"]])){
    
    # Create temporary data frame with only the crime of interest
    data_temp <- data[data[["Event.Clearance.Group"]] %in% crime,]
    

    if (length(data_temp$Longitude)==0) { next } # if no values, skip no next

    # Open file png file, escape name, ideal for unix machines, will still break on windows.
    crime = gsub("([/])","", crime)
    png(paste("Seattle Police 911_",crime,".png",sep=""), width = 1280, height = 1280)
    
    # Setup the Google map centered on all data.
    map <- GetMap(center=center, SCALE=2, zoom=11)
    
    # Transform Cords for Google Map Plotting
    coords <- LatLon2XY.centered(map, data_temp$Latitude, data_temp$Longitude)
    coords <- data.frame(coords)

    # Generate the kernel density map for the heatmap
    kd <- kde2d(coords$newX, coords$newY, n=1000)

    # Plot the map, heatmap, and points
    PlotOnStaticMap(map)
    image(kd, col=colors_a, add=T)
    points(coords$newX, coords$newY, pch=16, cex=0.3)

    # Save and close out the file
    dev.off()
}
