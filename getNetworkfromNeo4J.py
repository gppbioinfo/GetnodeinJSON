#!/usr/bin/python3 env

'''
' This program retrieve the nodes and relations from Neo4J graph database and converted into JSON and CSV/TXT format for D3 visualization and tabular view in HTML
'
'''

import os
import sys
from json import dumps
from flask import Flask, g, Response, request
from neo4j.v1 import GraphDatabase, basic_auth
import re

#Setup connection with Neo4J by username and password
driver = GraphDatabase.driver("bolt://192.168.4.110:7687", auth=("neo4j", "prp"))


def get_nodes(tx, name):
  #Declaration of empty list for interactor A
  nodes = []
  #Declaration of empty list for interactor B  
  node2 = []
  #Declaration of empty list for relations or links between interactor A and B
  rels = []
  #Node number initialization
  i = 0
  #Declaration of empty list for temperatory nodes from graph database
  nodeb = []
  #Output file of retrived graph in JSON format and txt format for graph visualization in D3 and tabular view in html
  outjson = sys.argv[2]
  outtxt = sys.argv[3]
  #print(outjson, outtxt)
  ojson = open(outjson, 'w')
  otxt = open(outtxt, 'w')
  #Initial node query input from user through html form for graph search through gene name/symbol/uniprot ID/miRNA name/TF so on. 
  name = sys.argv[1]+".*"
  #name = re.sub(r'G','T',name)  
  #Append initial Interactor A in emppty node list
  nodes.append({"id": i, "name": sys.argv[1], "label": "Gene"})
  #format as a string and set label and property for node
  ids = ""+str(i)+"",""+ sys.argv[1] + "", "Gene" 
  #print(ids)
  #Append initial Interactor A label and Property in list
  node2.append(ids)
  
  #Initialization of target node number by incrementing one
  target = i 
  i += 1
  
  #Run match query to retrieve interacted nodes from graph database  
  for record in tx.run("MATCH (n {species :\'Zea mays\'}) WHERE n.name =~ {name} OPTIONAL MATCH (n)-[r]-(m) OPTIONAL MATCH (m)-[r]-(p) RETURN n.name, m.name ORDER BY m.name, p.name", name=name):   		
  #for record in tx.run("MATCH p=allShortestPaths((a {name:\'$name\'})<-[*..5]-(m)) RETURN m limit 11", name=name):    		
  
    #Append all nodes in empty list for interactor B
    nodeb.append(record["m.name"])
    
  #Loop iteration for interactor B to format different nodes in JSON style for miRNA/sRNA/gene        
  for named in nodeb:
      if "miR" in named:                  
        bnode = {"id": i, "name": named, "label" : "miRNA"}
        bnode1 = [""+str(i)+"",""+named+"", "miRNA"]
        #print(bnode1)
        try:
          source = nodes.index(bnode)
          #print(source)
        except ValueError:
          nodes.append(bnode)
          node2.append(bnode1)	  
          source = i
          i += 1
          #print("%s interacts %s" % (source, target))
          #print(nodes)
          #print(target)
      elif "chr" in named:
         bnode = {"id": i, "name": named, "label" : "sRNA"}
         bnode1 = [""+str(i)+"",""+named+"", "sRNA"]
        #print(bnode1)
         try:
           source = nodes.index(bnode)
           #print(source)
         except ValueError:
           nodes.append(bnode)
           node2.append(bnode1)	  
           source = i
           i += 1
           #print("%s interacts %s" % (source, target))
           #print(nodes)
           #print(target)
      elif "[0-9]" in named:
         bnode = {"id": i, "name": named, "label" : "sRNA"}
         bnode1 = [""+str(i)+"",""+named+"", "sRNA"]
        #print(bnode1)
         try:
           source = nodes.index(bnode)
           #print(source)
         except ValueError:
           nodes.append(bnode)
           node2.append(bnode1)	  
           source = i
           i += 1
           #print("%s interacts %s" % (source, target))
           #print(nodes)
           #print(target)
      else:
         bnode = {"id": i, "name": named, "label" : "Gene"}
         bnode1 = [""+str(i)+"",""+named+"", "Gene"]
        #print(bnode1)
         try:
           source = nodes.index(bnode)
           #print(source)
         except ValueError:
           nodes.append(bnode)
           node2.append(bnode1)	  
           source = i
           i += 1
           #print("%s interacts %s" % (source, target))
           #print(nodes)
           #print(target)
      #Fix relations position between target and source interactors	     
      rels.append({"target": target, "source" : source})
  #Final output in JSON format file    
  ojson.write (dumps({"nodes": nodes, "links": rels}, indent=4))    
  otxt.write (dumps({"data": node2}, indent=4))	  
	  
with driver.session() as session:
    session.read_transaction(get_nodes, sys.argv[1])



s
