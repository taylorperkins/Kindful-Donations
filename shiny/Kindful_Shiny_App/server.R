
# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)

donor_history <- readRDS("data/donor_history.RDS")
monthly_history <- readRDS("data/monthly_history.RDS")


shinyServer(function(input, output) {
  output$top_bottom <-  DT::renderDataTable({
               donor_history %>% 
               filter(category == input$top_or_bottom) %>% 
               filter(year == year(input$date_input[2])) %>% 
               filter(month == month(input$date_input[2])) %>% 
               mutate_if(is.numeric, round, 2) %>% 
               select(id, amount, prev_year_rolling, last_year_rolling, rolling_diff) %>% 
               rename("Donor ID" = id, 
                      "Amount Donated ($)" = amount,
                      "Amount Donated During Last 12 Months ($)" = prev_year_rolling,
                      "Amount Donated between 12 - 24 Months ($)" = last_year_rolling,
                      "Difference between Rolling Years ($)" = rolling_diff)
  })
  
  HTML("<hr>")
  
  output$monthly_history <-  DT::renderDataTable({
    monthly_history %>% 
      mutate_if(is.numeric, round, 2) %>% 
      arrange(year) %>% 
      arrange(month) %>% 
      select(id, amount, month, year) %>% 
      rename("Donor ID" = id,
             "Amount Donated ($)" = amount,
             "Month" = month,
             "Year" = year)
  })
  
})
