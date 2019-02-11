## Libraries used ####
library(tidyverse) 
library(lubridate)
library(stringr)
library(purrr)
library(dplyr)

### Function to load a file and append to a dataframe ####
loadAndMerge = function(file_path,file2, temp_df1 = NULL){

  print(paste0("Processing file Name : ",file2 ))
  temp_df2 = read.csv(paste0(file_path,file2), stringsAsFactors = FALSE)  
  
  if(is.null(temp_df1)) {
    return(temp_df2)
  }
  
  col_str1 = paste(colnames(temp_df1), collapse = "")
  col_str2 = paste(colnames(temp_df2), collapse = "")

    if(col_str1 == col_str2) {
    return (rbind(temp_df1,temp_df2))
  }
  
  for (col_name in colnames(temp_df1)){
    if (!col_name %in% colnames(temp_df2)) {
      temp_df2[[col_name]] = NA
      print(paste0("col added to temp_df2 : ", col_name))
    }
  }
  
  for (col_name in colnames(temp_df2)){
  if (!col_name %in% colnames(temp_df1)) {
    temp_df1[[col_name]] = NA
    print(paste0("col added to temp_df1 : ", col_name))
    }
  }
  return (rbind(temp_df1,temp_df2))
}

### Functin to look for .csv files in folder and load them iteratively ####
multiFileMerge = function(my_path, file_pattern){
  file_names <- list.files(path = my_path  ,pattern = file_pattern)
  print(file_names)
  df = NULL
  for (file_name in file_names)
    df <- loadAndMerge(my_path, file_name, df)
  return(df)
}



### Call the functin and load the filed in folder
setwd("/Users/RV/Documents/Radha/OneDrive\ -\ Cognizant/Personal/Learn/DataScience/NYC/classes/handson/Projects/WebScraping/f500/")
combined_df = multiFileMerge("./data/raw/", ".csv")

write.csv(combined_df,"./data/processed/merged_data2.csv", row.names = FALSE)

