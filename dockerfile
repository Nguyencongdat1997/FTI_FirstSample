FROM python
ADD . /datgatto
WORKDIR /datgatto
RUN pip install -r python_requirement.txt
CMD python post_crawl_server/post_server.py & python token_server/token_server.py