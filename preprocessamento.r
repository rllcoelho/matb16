require(readr)
require(SnowballC)
library(dplyr)
library(tidytext)
library(stopwords)
library(wordcloud)
library(tidyr)
library(ggplot2)

# Carrega dataset e seleciona as colunas relevantes, compondo-as num dataframe (nibble)
allProp <- read.csv("~/Downloads/allProp.csv", comment.char="#")
txtEmenta <- as.character(allProp[,'txtEmenta']) 
txtEmenta_df <- data_frame(txtEmenta)
txtEmenta_df[, 'txtExplicacaoEmenta'] = as.character(allProp[,'txtExplicacaoEmenta']) 
txtEmenta_df[, 'nome'] = as.character(allProp[,'nome']) 
txtEmenta_df[, 'id'] = as.character(allProp[,'id']) 

# Carrega uma lista de stopwrds pt-br e adiciona algumas que parecem ser bastante comuns nesse dataset
sw = data_frame(data_stopwords_stopwordsiso$br)
# Posso usar essas stopwords personalizadas ou não. A adição delas pode alterar o resultado.
meses = c('janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro')
added_sw = data_frame(word = c('lei', 'nº', 'art', 'dá', 'no', 'para', 'dispõe', 
                               'altera', 'aprova', 'providências', 'ato', 'institui', 
                               'inciso', 'providencias', 'à', meses, 'trata'))
names(sw)[1] = 'word'
sw = union(sw, added_sw)

# Organiza od dados no formato tidy
palavras_tf_idf = txtEmenta_df %>%
  unite(txtEmenta, c("txtEmenta", "txtExplicacaoEmenta"), sep = " ") %>%
  unnest_tokens(word, txtEmenta) %>%
  anti_join(sw) %>%
  #posso considerar os documentos por nome ou por id, basta alterar a coluna que será usada abaixo
  count(nome, word, sort = T) %>%
  #filter(!grepl('^\\d{2}\\.\\d{3}|\\s\\d{2}|\\d{2}\\s', word)) %>%
  filter(!grepl('^\\d+', word)) %>%
  bind_tf_idf(word, nome, n) %>%
  arrange(desc(tf_idf)) %>%
  filter(nome %in% c("PL 6383/2016", "PL 6384/2016", "PL 6385/2016", "PL 6386/2016", 
                     "PL 6388/2016", "PL 6387/2016"))

palavras_tf_idf %>%
  arrange(desc(tf_idf)) %>%
  mutate(word = factor(word, levels = rev(unique(word)))) %>% 
  #top_n(1) %>%
  group_by(nome) %>% 
  top_n(10) %>% 
  ungroup %>%
  ggplot(aes(word, tf_idf, fill = nome)) +
  geom_col(show.legend = FALSE) +
  labs(x = NULL, y = "tf-idf") +
  facet_wrap(~nome, ncol = 2, scales = "free") +
  coord_flip()

as.data.frame(palavras_tf_idf)[1:50,]
