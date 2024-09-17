TITULO = "table.titulo_superior"
PESQUISA = "//div[@class='input-group custom-search-form']//div[@class='visible-lg']//input[contains(@class,'form-control ng-pristine')]"

LIMPAR_TUDO = "//button[@ng-if='acesso_publico' and @data-target='#limpar_tudo']"
PESQUISAR = "//span[@class='visible-lg input-group-btn']//button[@id='btnPesquisar']"
PRIMEIRO_RESULTADO = "(//div[@class='table-responsive']//tr[@ng-repeat='documento in PesquisaSolr.documentos'])[1]//a[@target='unico' and @class='ng-scope']"


TABELA_INFO_PROCESSO = "//table[@id='tab_proc']"
LINHAS_TABELA_INFO_PROCESSO = "//table[@id='tab_proc']//tr"
LINHAS_TABELA_MOVIMENTACOES = "//div[@id='div_results']//table[@id='tab_mov']//tr"
