setwd('/Users/franco/Downloads')

library(rgeos)
library(sp)
library(rgdal)
library(sf)
library(stringr)


# district boundaries shapefile
shp = read_sf('Council Districts/geo_export_0c7f1f6c-b750-4d98-beb8-25c3d5f676e8.shp')
shp = read_sf('Council Districts/geo_export_37659960-a4e3-4f59-a845-edebabe31a30.shp')

dat = read.csv("arrests_2018.csv")

# split longitude and latitude to seperate columns
dat$Location = as.character(dat$Location)
split_str = str_split(dat$Location, ",")
mat = matrix(unlist(split_str), ncol=2, byrow=TRUE)
temp = as.data.frame(mat)

dat$Long = temp$V1
dat$Lat = temp$V2

# remove paranthesis
dat$Long = str_remove(dat$Long, "[(]")
dat$Lat = str_remove(dat$Lat, "[)]")
dat$Location = NULL

dat$Long = as.numeric(dat$Long)
dat$Lat = as.numeric(dat$Lat)

coord = dat[, c("Lat", "Long")]
coord = as.data.frame(coord)


coordinates = do.call("st_sfc",c(lapply(1:nrow(coord), 
                          function(i) {st_point(as.numeric(coord[i, ]))}), list("crs" = 4326))) 

coords_trans = st_transform(coordinates, 2163)
shp_pl = st_transform(shp, 2163) 

dat$CouncilID <=apply(st_intersects(shp_pl, coords_trans, sparse = FALSE), 2, 
                     function(col) { 
                       shp[which(col), ]$district
                     })
dat$CouncilID = as.character(dat$CouncilID)
write.csv(dat, "arrest_filtered.csv")


# refrence
## https://gis.stackexchange.com/questions/282750/identify-polygon-containing-point-with-r-sf-package