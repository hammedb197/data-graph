
from neo4j import GraphDatabase
# cypher query to save to db
query = '''
        MERGE (u:Content {content: $content}) 
        MERGE (s:Sentiment {sent:$sentiment_})
        MERGE (e:Entity {entity:$title})
        FOREACH (person IN $person | MERGE (e)-[:CONNECTED_PERSON]->(p: Person {person: person.PERSON}))
        FOREACH (location IN $location | MERGE (e)-[:RELATED_LOCATION]->(l:Location {location:location.GPE}))
        FOREACH (organization IN $organization | MERGE (e)-[:CONNECTED_TO_ORG]->(o:Organization {organization:organization.ORG }))
        MERGE (u)-[:TEXT_ABOUT]->(e)<-[:SENT_ABOUT]-(s)
  
  
      '''
#       save to database
def sendToNeo4j(*args, **kwargs):
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'graph'))
    db = driver.session()
    consumer = db.run(query, *args, **kwargs).consume()
    
    