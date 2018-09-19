FROM python
ADD . /app
WORKDIR /app
RUN pip install -r python_requirement.txt
CMD python post_crawl_server/post_server.py