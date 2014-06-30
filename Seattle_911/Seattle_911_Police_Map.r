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

# Title wrapping helper function 
titlewrap <- function(x, ...) paste(strwrap(x, ...), collapse = "\n")


# Download the relevant Seattle Public Data into the data directory
if(!file.exists("data")){
    dir.create("data")
}
file_url <- "https://data.seattle.gov/api/views/3k2p-39jp/rows.csv?accessType=DOWNLOAD"
file_loc <- "./data/seattle_911_police_response.csv"
if(!file.exists(file_loc)){
    download.file(file_url,destfile=file_loc,method="curl")
    cat("## Date Downloaded", as.character(Sys.Date()),'\n',file=file_loc,append=T)
}

# Setup the output folder for the images we are plotting
if(!file.exists("output")){
    dir.create("output")
}

# Read the file into memory, last I checked this file is about 200 MB. May need to start subsampling
data <- read.csv(file=file_loc, header=T, comment.char="#", na.strings = "NULL", skipNul=T, stringsAsFactors=F)

# Clean up the dataset, remove leading and trailing white space and remove empty location data.
data[["Event.Clearance.Group"]] <- as.factor(gsub("^\\s+|\\s+$", "",data[["Event.Clearance.Group"]]))
data[["Event.Clearance.Description"]] <- as.factor(gsub("^\\s+|\\s+$", "",data[["Event.Clearance.Description"]]))
data <- data[complete.cases(data["Latitude"],data["Longitude"]),]

# Center for the Google Map
center <- sapply(c(data["Latitude"],data["Longitude"]),function(x) (max(x)+min(x))/2)

# Setup the Google map centered on all data.
map <- GetMap(center=center, SCALE=2, zoom=11)

# Hard coded limits to make all of the kernel densities cover the same area.
lims <- matrix(c(range(data$Latitude),range(data$Longitude)),nrow=2)
lims <- unlist(LatLon2XY.centered(map, lims[,1],lims[,2]))


# Setup Colors from Green to Red.
# Add transparency
colors <- rev(colorRampPalette(brewer.pal(8, 'RdYlGn')(16)))
colors_a <-alpha(colors,0.5)

# Loop through each of the crime categories. Create a heatmap for each one and save them as a new png file.
for (crime in levels(data[["Event.Clearance.Description"]])){
    
    # Create temporary data frame with only the crime of interest
    data_temp <- data[data[["Event.Clearance.Description"]] %in% crime,]
    

    if (length(data_temp$Longitude)==0) { next } # if no values, skip no next
    if (crime == "" | crime == "NULL") {next } # skip the two null sets


    # Open file png file, escape name, ideal for unix machines, will still break on windows.
    crime = gsub("([/])","-", crime)
    png(paste("output/Seattle Police 911_",crime,".png",sep=""), width = 1280, height = 1280)
    
    
    # Transform Cords for Google Map Plotting
    coords <- LatLon2XY.centered(map, data_temp$Latitude, data_temp$Longitude)
    coords <- data.frame(coords)

    # Generate the kernel density map for the heatmap
    kd <- kde2d(coords$newX, coords$newY, n=500, lims=lims)

    # Plot the map, heatmap, and points
    PlotOnStaticMap(map)
    points(coords$newX, coords$newY, pch=16, cex=0.3)
    image(kd, col=colors_a, add=T)

    title(main=titlewrap(crime,20), cex.main=3, line=-85.5, col.main="black")
    title(main=paste("n =",length(data_temp$Longitude)), cex.main=0.75, line=-86.5)

    # Save and close out the file
    dev.off()
}
