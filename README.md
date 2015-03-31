
## Basic Django Template Project Setup

```bash
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
export WORKON_HOME=/XXX/python-env
source /usr/local/bin/virtualenvwrapper.sh
export PATH=/usr/local/bin/:$PATH
```
Clone the repository from github and set up the python environment and dependencies.

```bash
mkvirtualenv django_template_env
pip install -r requirements.txt
```
The following set up assumes a GMOD Chado schema installation with the gene, relationship and sequence ontologies loaded.
Edit the database settings in django_template/settings_secret.py.template and copy into place.

```bash
cp django_template/settings_secret.py.template  django_template/settings_secret.py
```

```bash
insert into organism ( abbreviation, genus, species, common_name ) values ( 'H.sapiens', 'Homo', 'sapiens_GRCh38', 'human_GRCh38');
insert into organism ( abbreviation, genus, species, common_name ) values ( 'M.musculus', 'Mus', 'musculus_mm10', 'mouse_mm10');
```

Download chromosome data and populate the database:

```bash
curl ftp://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/chromInfo.txt.gz > tmp/chromInfo_human.txt.gz
curl ftp://hgdownload.cse.ucsc.edu/goldenPath/mm10/database/chromInfo.txt.gz  > tmp/chromInfo_mouse.txt.gz

curl ftp://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/cytoBand.txt.gz  -o tmp/cytoBand_human.txt.gz
curl ftp://hgdownload.cse.ucsc.edu/goldenPath/mm10/database/cytoBand.txt.gz  -o tmp/cytoBand_mouse.txt.gz

curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-AA-assoc_tableGFF -o tmp/Hs_GRCh38-AA-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-ATD-assoc_tableGFF -o tmp/Hs_GRCh38-ATD-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-CEL-assoc_tableGFF -o tmp/Hs_GRCh38-CEL-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-CRO-assoc_tableGFF -o tmp/Hs_GRCh38-CRO-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-JIA-assoc_tableGFF -o tmp/Hs_GRCh38-JIA-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-MS-assoc_tableGFF -o tmp/Hs_GRCh38-MS-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-PBC-assoc_tableGFF -o tmp/Hs_GRCh38-PBC-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-PSO-assoc_tableGFF -o tmp/Hs_GRCh38-PSO-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-RA-assoc_tableGFF -o tmp/Hs_GRCh38-RA-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-SLE-assoc_tableGFF -o tmp/Hs_GRCh38-SLE-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-T1D-assoc_tableGFF -o tmp/Hs_GRCh38-T1D-assoc_table.gff
curl http://www.immunobase.org/regions/htdocs/downloads/Hs_GRCh38-UC-assoc_tableGFF -o tmp/Hs_GRCh38-UC-assoc_table.gff
```

Then the populate_db command line argument can be used to load the data:

```bash
python manage.py populate_db --help
python manage.py populate_db --chr tmp/chromInfo_human.txt.gz --org human_GRCh38
python manage.py populate_db --chr tmp/chromInfo_mouse.txt.gz --org mouse_mm10
python manage.py populate_db --bands tmp/cytoBand_human.txt.gz --org human_GRCh38 
python manage.py populate_db --bands tmp/cytoBand_mouse.txt.gz --org=mouse_mm10
python manage.py populate_db --disease tmp/disease.list

python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-AA-assoc_table.gff
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-ATD-assoc_table.gff
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-CEL-assoc_table.gff
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-CRO-assoc_table.gff 
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-JIA-assoc_table.gff 
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-MS-assoc_table.gff 
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-PBC-assoc_table.gff 
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-PSO-assoc_table.gff 
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-RA-assoc_table.gff 
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-SLE-assoc_table.gff 
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-T1D-assoc_table.gff 
python manage.py populate_db --org human_GRCh38 --gff tmp/Hs_GRCh38-UC-assoc_table.gff 

```

Run the server, e.g.:

```bash
python manage.py runserver localhost:9000
```

In a browser try http://localhost:9000/bands/cached/human_GRCh38/

```bash
./manage.py makemigrations
./manage.py migrate
./manage.py test db.tests bands.tests search.tests marker.tests -v3
```

### Using Caching

To get the caching to work memcache needs to be installed:
```
sudo apt-get install memcached
```

### Elasticsearch

Download the latest version (http://www.elasticsearch.org/download). Install and start, e.g.

```
sudo dpkg -i elasticsearch-1.4.2.deb
sudo /etc/init.d/elasticsearch start
```

Check the server is running:

```
curl http://127.0.0.1:9200/
curl 'http://127.0.0.1:9200/_cat/indices?v'
```

Edit the configuration file (i.e. elasticsearch.yml). As an example of indexing see the following 
help command:

```
python manage.py index_search --help
```
