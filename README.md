Por enquanto há apenas o crawler de URLs, que é responsável por descobrir
todas as páginas internas do site.

Para indexação você deve:

1) Inserir, utilizando o admin, o endereço http://www.olavodecarvalho.org/index.html
e salvar.

2) Executar o comando $python manage.py crawl fetch parse.

OBS1: Atenção para a configuração do manage.py (está importanto configurações
de 'odc.settings.dev_pedro').

OBS2: A app não está ainda em condições de ser distribuída para uso genérico.

OBS3: A app não foi projetada para lidar com um número grandioso de URLs. Não
há, portanto, uso de threads ou de processos paralelos.