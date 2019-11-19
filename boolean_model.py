 
# coding=utf-8
# @author: Luiz Henrique Dias Lima - 11721bsi261

import sys
import os

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem.api import StemmerI

# nltk.download("rslp")
# nltk.download("punkt")
# nltk.download("stopwords")


class BooleanModel:
    def __init__(self, p_file1, p_file2):
        # Recebe o nome do arquivo de base passado pela linha de comando
        self.p_file1 = p_file1
        # Recebe o arquivo que contém a consulta
        self.p_file2 = p_file2
        # Dicionário com o nome do arquivo e seu respectivo número de sequência
        self.v_doc_list = {}
        # Recebe as frases de cada arquivo
        self.v_files_Sentence = []
        # Recebe as palavras não stopwords de cada arquivo
        self.v_non_stopwords = []
        # Recebe as stopwords contidas no arquivo
        self.v_stopwords = []
        # Dicionário que recebe a palavra não stopword.
        self.v_inverted_index = {}

    # @func: ir_read_data_file
    # @param: //
    # @returns: //
    # A função lê todos os arquivos contidos em f, o qual recebe uma lista sem linhas em branco.
    # Cada nome de arquivo é uma chave para o dicionário e o valor para cada chave é o número de 
    # sequência do arquivo.
    # Caso haja um erro na execução, o programa é encerrado. 
    def ir_read_data_file(self):
        count = 1
        try:

            f = self.ir_remove_white_space()
            for file_name in f:
                if os.path.isfile('./' + file_name.replace('\n', '')):
                    self.v_doc_list[file_name.replace('\n', '')] = count
                    count+=1
                else:
                    raise FileNotFoundError('')           
        except FileNotFoundError as e_file:
            print(f'{e_file} Não foi possível encontrar o arquivo solicitado {file_name}')
            print('Abortando execução ...')
            exit(1)
        
    # @func: ir_remove_white_space
    # @param: //
    # @returns: list
    # Essa função remove todos os espaços em brancos contidos no arquivo passado pela linha de comando;
    # sem esse devido tratamento, arquivos com linhas em branco fariam com que o programa encerrasse, para evitar isso
    # a função retira essas linhas.
    def ir_remove_white_space(self):

        try:
            list_items_aux = []
            list_file_items = []
            f = open(self.p_file1, 'r', encoding= 'utf-8')
            for file_name in f:
                list_items_aux.append(file_name.strip())

            for i in list_items_aux:
                if i != '':
                    list_file_items.append(i)    
            return list_file_items
        except IOError:
            print(f'Não foi possível abrir o arquivo {f}')        
        finally:
            f.close()    

    # @func: ir_removeDuplicates()
    # @param: //
    # @returns: //
    # A função remove os itens duplicados contidos em v_non_stopwords
    def ir_removeDuplicates(self):
        v_non_stopwords_aux = []
        for index in self.v_non_stopwords:
            if index not in v_non_stopwords_aux:
                v_non_stopwords_aux.append(index)
        
        self.v_non_stopwords = v_non_stopwords_aux
        del v_non_stopwords_aux
    
    # @func: t_read_files
    # Lê de cada arquivo o conteúdo presente e, então, retira as stopwords
    # contidas em cada arquivo.
    # Após a remoção das stopwords, há a retirada dos radicais das palavras
    # remanescentes em v_files_Sentence, esses serão armazenados em 
    # v_non_stopwords
    # @param: //
    # @returns: //
    def ir_read_files(self):
     
        try:
            for i in self.v_doc_list.keys():
                v_content_file_aux = open(i, 'r', encoding= 'utf-8')
                self.v_files_Sentence.append(v_content_file_aux.read().replace('\n', ' ')) 
            
        except IOError:
            print(f'Não foi possível encontrar o arquivo {v_content_file_aux}')
        finally:
            v_content_file_aux.close()    

  
        stopwords = nltk.corpus.stopwords.words("portuguese")
        stemmer = nltk.stem.RSLPStemmer()
      
        for frase in self.v_files_Sentence:
           tokens = [t for t in word_tokenize(frase.lower()) if t.isalpha()]

           for index in tokens:
               if index not in stopwords:
                   self.v_non_stopwords.append(stemmer.stem(index))
               else:
                   self.v_stopwords.append(index)     

        self.ir_removeDuplicates()
        
    # @func: ir_build_Inverted_Index
    # @param: //
    # @returns: //
    # A função cria um índice invertido.
    def ir_build_Inverted_Index(self):
        tokens_file_dic = {}
     
        stemmer = nltk.stem.RSLPStemmer()
        try:
            for file_name in self.v_doc_list.keys():
                sentence = open(file_name, 'r', encoding= 'utf-8')
                tokens = [t for t in word_tokenize(sentence.read().lower()) if t.isalpha()]
                tokens_file_dic[self.v_doc_list[file_name]] = [] 
                for i in tokens:
                    if i not in self.v_stopwords:
                        tokens_file_dic[self.v_doc_list[file_name]].append(stemmer.stem(i))
        except FileNotFoundError as e_file:
            print(f"{e_file} Não foi possível abrir o arquivo {sentence}")    
        finally:
            sentence.close()
	       

        for i, v in tokens_file_dic.items():
            for non_stop  in self.v_non_stopwords:
                for term in v:
                    if non_stop == term:
                    # Se não está presente no dicionário, então adicione-a ao diacionário
                    # e crie um um outro dicionário para cada palavra(e.g. {term: {arquivo: 1}})
                        if non_stop not in self.v_inverted_index:
                            self.v_inverted_index[non_stop] = {}
                            self.v_inverted_index[non_stop][i] = 1 
                    # Se não se a palavra já exitir e i(que o número do arquivo) já fora inserido anteriormente, incremente de 1    
                        elif i in self.v_inverted_index[non_stop].keys():   
                            sum_aux = self.v_inverted_index[non_stop][i]
                            sum_aux += 1                            
                            self.v_inverted_index[non_stop][i] = sum_aux
                    # Se não, adicione o número do arquivo à stopword e atribua [1](e.g. {term: {arquivo: 1, arquivo2: 1}})   
                        else:
                            self.v_inverted_index[non_stop][i] = 1    
                        
    # @func: ir_build_Inverted_Index_File
    # @param: //
    # @returns: //
    # Essa função cria o arquivo contendo o indice invertido
    # em caso de erro é programa é encerrado e o arquivo não é criado.
    def ir_build_Inverted_Index_File(self):
        try:
            v_file = open('indice.txt',  'w', encoding= 'utf-8')
            for k, v in self.v_inverted_index.items():
                v_file.write(str(k) + ": ")
                for i, j in v.items():
                    v_file.write(str(i) + "," + str(j) + " ") 
                v_file.write('\n')    

            print("Indice invertido criado com sucesso em: ", os.path.abspath("indice.txt"))    
        except IOError as e_file:
            print(f"Não foi possível criar o arquivo {e_file}")
        finally:
            v_file.close()

    # ir_answer_query()
    # Pega o conteúdo do arquivo que contém a query
    # e, através do v_inverted_index, reponde a query
    # É importante pegar o nome do arquivo a partir de seu id
    # o qual está armazenado em v_doc_list
    # Antes de extrair o radical é importante tratar os operadores contidos na consulta.
    def ir_answer_query(self):
        try:
            v_query_list = []
            if os.path.isfile(self.p_file2):
                f = open(self.p_file2, 'r', encoding= 'utf-8')
            else:
                raise FileNotFoundError(self.p_file2)    
            

            v_query = f.read().lower()
            
            stopwords = nltk.corpus.stopwords.words("portuguese")
            stemmer = nltk.stem.RSLPStemmer()
            tokens = word_tokenize(v_query)


            # Remoção das stopwords da consulta
            for q_stop in tokens:
                if q_stop not in stopwords:
                     v_query_list.append(stemmer.stem(q_stop))
            # Cria uma nova string com os radicais e sem as stopwords
            v_query = " ".join(v_query_list)
            # Tratamento de queries com |
            # e outros operadores inclusos
            if '|' in v_query:
                v_set_inter = set()
                v_set_union_aux = set()
                v_set_aux = set()
                v_query_list = v_query.split('|')
               
                for i in range(0, len(v_query_list)):
                    if '&' in v_query_list[i]:
                        v_set_aux = self.ir_search_items_and(v_query_list[i])
                        for i in v_set_aux:
                            v_set_inter.add(i)
                    else:
                        v_set_aux = self.ir_search_item(v_query_list[i])
                        for i in v_set_aux:
                            v_set_union_aux.add(i)
                
                if (len(v_set_inter) == 0) and (len(v_set_union_aux) > 0):
                    self.ir_create_query_file(v_set_union_aux) 
                elif (len(v_set_inter) > 0) and (len(v_set_union_aux) == 0):
                    self.ir_create_query_file(v_set_inter)              
                elif (len(v_set_inter) > 0) and (len(v_set_union_aux) > 0):
                    v_set_union_aux = v_set_union_aux.union(v_set_inter)
                    self.ir_create_query_file(v_set_union_aux)   

            #Tratamento para consultas que não possuam o |   
            # query do tipo a & b
            elif ('|' not in v_query) and ('&' in v_query):
                v_set_aux = self.ir_search_items_and(v_query)
                self.ir_create_query_file(v_set_aux)     
            # query do tipo !a 
            elif ('|' not in v_query) and ('&' not in v_query) and ('!' in v_query):
                v_set_aux = self.ir_search_items_not(v_query)
                self.ir_create_query_file(v_set_aux)
            # query do tipo a  
            else:
                v_set_aux = self.ir_search_item(v_query)
                self.ir_create_query_file(v_set_aux)    

            f.close()           
        except FileNotFoundError as e_file:
            print(f'Não foi possível abrir/encontrar o arquivo {e_file}')   
        
            

    # @func: ir_search_item
    # @param: Recebe a subquery de ir_answer_query
    # @returns: set()
    # A função pesquisa pelo item. o qual é passado como argumento, no
    # dicionário invertido, e retorna o conjunto com os arquivos que satisfaçam
    # a pesquisa.

    def ir_search_item(self, v_sub_query):
        v_set_aux = set()
        if '!' in v_sub_query:
            v_set_aux = self.ir_search_items_not(v_sub_query)
        else:    
            for k, v in self.v_inverted_index.items():
                for file_id in v.keys():   
                    if k == v_sub_query.replace(' ', ''):
                        v_set_aux.add(file_id)
                  

        return v_set_aux   


    # @func: ir_search_item_not
    # @param: v_sub_query, recebe a subquery de ir_answer_query
    # @returns: set()
    # A função pesquisa pelo item. o qual é passado como argumento, no
    # dicionário invertido, e retorna o conjunto com os arquivos que não contenham v_sub_query
    # a pesquisa.
    def ir_search_items_not(self, v_sub_query):
        v_set_aux = set()
        v_sub_query = v_sub_query.replace("!", "")
        for k, v in self.v_inverted_index.items():
            for file_id in v.keys():   
                if k == v_sub_query.replace(' ', ''):
                    v_set_aux.add(file_id)

        v_set_universe = self.ir_get_file_id()

        v_set_aux = v_set_universe.difference(v_set_aux)   
        return v_set_aux          
    # @func: ir_get_file_id
    # @param: //
    # @returns: set()
    # A função retorna um conjunto com todos os num. de seq. arquivos presentes na base
    def ir_get_file_id(self):
        v_file_id_set = set()
        for k, v in self.v_inverted_index.items():
            for file_id in v.keys():
                v_file_id_set.add(file_id)

        return v_file_id_set        
    
    # @func: ir_search_item_and
    # @param: v_sub_query, recebe a subquery de ir_answer_query
    # @returns: set()
    # A função pesquisa pelo item. o qual é passado como argumento, no
    # dicionário invertido, e retorna a intersecção dos conjuntos com os arquivos que contenham v_sub_query
    def ir_search_items_and(self, v_sub_query):
        v_set_and_aux = set()
        v_set_inter_1 = set()
        v_final_set = set()

        count_and = 0
        count_not_and = 0
        
        v_list_aux_and = v_sub_query.split('&')
        
        v_set_and_aux = self.ir_get_file_id()
        v_set_and_not_aux = self.ir_get_file_id()
        
        for i in range(0, len(v_list_aux_and)):
            if '!' in v_list_aux_and[i]:
                v_set_inter_1 = self.ir_search_items_not(v_list_aux_and[i].replace('!', ""))
                v_set_and_not_aux = v_set_and_not_aux.intersection(v_set_inter_1)

                count_not_and +=1
            else:

                v_searched_items_0 = self.ir_search_item(v_list_aux_and[i])
                v_set_and_aux = v_set_and_aux.intersection(v_searched_items_0)                

                count_and += 1

        if (count_and > 0) and (count_not_and > 0):
            v_final_set =  v_set_and_aux.intersection(v_set_and_not_aux) 
        elif (count_and == 0) and (count_not_and > 0):
            v_final_set = v_set_and_not_aux
        elif (count_and > 0) and (count_not_and == 0):
            v_final_set = v_set_and_aux         

    
        return v_final_set            
    # @func: ir_create_query_file
    # @param: p_query, recebe o set, contendo a intersecção, diferença ou união 
    # @returns: //
    # Essa função cria o arquivo contendo a resposta para a consulta lida no arquivo consulta.txt
    # Em caso de erro na criação do arquivo o programa é abortado. 
    def ir_create_query_file(self, p_query):
        # Primeiro converter o set em lista
        v_query_list_files_id = list(p_query)

        # v_query_list_files_name recebe o nome dos arquivos
        v_query_list_files_name = []
        # Dado que para cada arquivo foi associado um id, agora é só comparar
        # a lista com os id com os id's contidos em v_doc_list
        for k, v in self.v_doc_list.items():
            for id_index in v_query_list_files_id:
                if v == id_index:
                    v_query_list_files_name.append(k)
        
        try:
            f = open('resposta.txt', 'w+', encoding= 'utf-8')
            count = len(v_query_list_files_name)
            f.write(str(count))
            f.write('\n')
            for i in v_query_list_files_name:
                f.write(i)
                f.write('\n')

            print("Arquivo criado com sucesso em: ", os.path.abspath("resposta.txt"))    

        except IOError as e_error:
            print(f'{e_error} Não foi possível criar o arquivo {f}')
        finally:
            f.close()

# Fim da Classe BooleanModel

      
# @func: t_verify_arg()
# Função que verifica se a quantidade de argumentos passados está correta
# Se sim, é retornada uma lista contendo os nomes do argumentos; se não,
# o programa é finalizado.
# @param: //
# @returns: //
          
def ir_verify_arg():
    if len(sys.argv[1:]) == 2:
        return sys.argv[1:]
    else:
        print("Devem ser passados 2 argumentos na linha de comando")  
        exit(1)  


if __name__ == "__main__":
    v_arg_list = ir_verify_arg()
    boolean_Model = BooleanModel(v_arg_list[0], v_arg_list[1])
    boolean_Model.ir_read_data_file()
    boolean_Model.ir_read_files()
   
    boolean_Model.ir_build_Inverted_Index()
    print()
    boolean_Model.ir_build_Inverted_Index_File()
    print()
    boolean_Model.ir_answer_query()