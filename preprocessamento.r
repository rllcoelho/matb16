require(readr)
require(SnowballC)
library(dplyr)
library(tidytext)
library(stopwords)
library(wordcloud)
library(tidyr)

allProp <- read.csv("~/Downloads/allProp.csv", comment.char="#")

txtEmenta <- as.character(allProp[,'txtEmenta']) 

txtEmenta_df <- data_frame(txtEmenta)
txtEmenta_df[, 'txtExplicacaoEmenta'] = as.character(allProp[,'txtExplicacaoEmenta']) 
txtEmenta_df[, 'nome'] = as.character(allProp[,'nome']) 
txtEmenta_df[, 'id'] = as.character(allProp[,'id']) 

meses = c('janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro')

sw = data_frame(data_stopwords_stopwordsiso$br)
added_sw = data_frame(word = c('lei', 'nº', 'art', 'dá', 'no', 'para', 'dispõe', 
                               'altera', 'aprova', 'providências', 'ato', 'institui', 
                               'inciso', 'providencias', 'à', meses, 'trata'))
names(sw)[1] = 'word'
sw = union(sw, added_sw)

palavras = txtEmenta_df %>%
  unite(txtEmenta, c("txtEmenta", "txtExplicacaoEmenta"), sep = " ") %>%
  unnest_tokens(word, txtEmenta) %>%
  anti_join(sw) %>%
  count(id, word, sort = T) %>%
  bind_tf_idf(word, id, n) %>%
  arrange(desc(tf_idf))

as.data.frame(palavras)[1:50,]

stopwords::
stopwords_getsources()
