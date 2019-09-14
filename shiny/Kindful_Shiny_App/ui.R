
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)
library(shinythemes)
library(lubridate)
library(dplyr)
library(DT)

shinyUI(fluidPage(theme = shinytheme("flatly"),

  # Application title
  titlePanel("Kindful Donor Tracking"),
  

  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
      
      img(src='kindful_symbol.png', align = "left"),
    
      
      dateRangeInput("date_input",
                     "Date Selection:",
                     min = '2013-10-08',
                     max = today(),
                     start = as_date('2018-05-09') - 365,
                     end = '2018-05-09'),
      selectInput('top_or_bottom',
                  "Choose between top donors or largest missing donors:",
                  choices = c('Top 5 Donors' = 'top',
                              'Bottom 5 Donors' = 'bottom'),
                  selected = 'Top Donors',
                  multiple = FALSE)
      

      
    ),

    # Show a plot of the generated distribution
    mainPanel(
      DT::dataTableOutput("top_bottom"),
      DT::dataTableOutput("monthly_history")
    )
  )
))
