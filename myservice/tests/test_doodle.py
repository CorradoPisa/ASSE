import unittest
import json
from flask import request, jsonify
from myservice.app import app as tested_app


class TestApp(unittest.TestCase):

    def test1(self): #allpolls
        app = tested_app.test_client()

        #create 3 doodles
        reply = app.post('/doodles', 
                         data=json.dumps({"title" : "poll1", 
                                          "options" : ["1", "2", "3"]
                                          }), 
                         content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body['pollnumber'], 1)

        reply = app.post('/doodles', 
                         data=json.dumps({"title" : "poll2", 
                                          "options" : ["1", "2"]
                                          }), 
                         content_type='application/json')      
        
        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body['pollnumber'], 2)

        reply = app.post('/doodles', 
                         data=json.dumps({"title" : "poll3", 
                                          "options" : ["pizza", "disco"]
                                          }), 
                         content_type='application/json')        
                        
        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body['pollnumber'], 3)

        #get the three doodles
        reply = app.get('/doodles')                       
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {
                                "activepolls": [
                                    {
                                        "id": 1,
                                        "options": {
                                            "1": [],
                                            "2": [],
                                            "3": []
                                        },
                                        "title": "poll1",
                                        "winners": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    {
                                        "id": 2,
                                        "options": {
                                            "1": [],
                                            "2": []
                                        },
                                        "title": "poll2",
                                        "winners": [
                                            "1",
                                            "2"
                                        ]
                                    },
                                    {
                                        "id": 3,
                                        "options": {
                                            "disco": [],
                                            "pizza": []
                                        },
                                        "title": "poll3",
                                        "winners": [
                                            "pizza",
                                            "disco"
                                        ]
                                    }
                                ]
                            } )

    def test2(self): #single poll
        app = tested_app.test_client()

        # retrieve existing doodle GET
        reply = app.get('/doodles/2')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {
                                "id": 2,
                                "options": {
                                    "1": [],
                                    "2": []
                                },
                                "title": "poll2",
                                "winners": [
                                    "1",
                                    "2"
                                ]
                            })

        #retrieve non-existing doodle GET
        reply = app.get('/doodles/12')
        self.assertEqual(reply.status_code, 404)
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,{
                                "code": 404,
                                "description": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
                                "message": "404 Not Found: The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again."
                            })

        # vote ok
        reply = app.put('/doodles/2',data=json.dumps( {
                                                        "person" : "fred",
                                                        "option" : "1"
                                                    }), 
                         content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body,{
                                "winners": [
                                    "1"
                                ]
                            }
                        )   

        # vote ok
        reply = app.put('/doodles/2',data=json.dumps( {
                                                        "person" : "fred",
                                                        "option" : "2"
                                                    }), 
                         content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body,{
                                "winners": [
                                    "1",
                                    "2"
                                ]
                            }
                        )   
        # vote ok
        reply = app.put('/doodles/2',data=json.dumps( {
                                                        "person" : "barney",
                                                        "option" : "1"
                                                    }), 
                         content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(body,{
                                "winners": [
                                    "1"
                                ]
                            }
                        )  
        # vote replica
        reply = app.put('/doodles/2',data=json.dumps( {
                                                        "person" : "barney",
                                                        "option" : "1"
                                                    }), 
                         content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))

        self.assertEqual(reply.status_code, 400)
        self.assertEqual(body,{
                                "code": 400,
                                "description": "The browser (or proxy) sent a request that this server could not understand.",
                                "message": "400 Bad Request: The browser (or proxy) sent a request that this server could not understand."
                            }
                        )   

        # vote non-existing option                
        reply = app.put('/doodles/2',data=json.dumps( {
                                                        "person" : "wilma",
                                                        "option" : "8"
                                                    }), 
                         content_type='application/json')

        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(body,{
                                "code": 400,
                                "description": "The browser (or proxy) sent a request that this server could not understand.",
                                "message": "400 Bad Request: The browser (or proxy) sent a request that this server could not understand."
                            }
                        )   
        # delete doodle
        reply = app.delete('/doodles/2')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,{
                                "winners": [
                                    "1"
                                ]
                            }
                        )      

        reply = app.get('/doodles')                        
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body, {
                                "activepolls": [
                                    {
                                        "id": 1,
                                        "options": {
                                            "1": [],
                                            "2": [],
                                            "3": []
                                        },
                                        "title": "poll1",
                                        "winners": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    {
                                        "id": 3,
                                        "options": {
                                            "disco": [],
                                            "pizza": []
                                        },
                                        "title": "poll3",
                                        "winners": [
                                            "pizza",
                                            "disco"
                                        ]
                                    }
                                ]
                            } )  

        # delete previously doodle
        reply = app.delete('/doodles/2')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 410)
        self.assertEqual(body,{
                                "code": 410,
                                "description": "The requested URL is no longer available on this server and there is no forwarding address. If you followed a link from a foreign page, please contact the author of this page.",
                                "message": "410 Gone: The requested URL is no longer available on this server and there is no forwarding address. If you followed a link from a foreign page, please contact the author of this page."
                            }
                        ) 
        
        #delete non-existing doodle
        reply = app.delete('/doodles/12')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 404)
        self.assertEqual(body,{
                                "code": 404,
                                "description": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
                                "message": "404 Not Found: The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again."
                            })

        #get previously existing doodle
        reply = app.get('/doodles/2')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 410)
        self.assertEqual(body,{
                                "code": 410,
                                "description": "The requested URL is no longer available on this server and there is no forwarding address. If you followed a link from a foreign page, please contact the author of this page.",
                                "message": "410 Gone: The requested URL is no longer available on this server and there is no forwarding address. If you followed a link from a foreign page, please contact the author of this page."
                            }
                        )          

    def test3(self): #person poll
        app = tested_app.test_client()
        # vote ok
        reply = app.put('/doodles/1',data=json.dumps( {
                                                        "person" : "fred",
                                                        "option" : "1"
                                                    }), 
                         content_type='application/json')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,{
                                "winners": [
                                    "1"
                                ]
                            }
                        )   

        # vote ok
        reply = app.put('/doodles/1',data=json.dumps( {
                                                        "person" : "fred",
                                                        "option" : "2"
                                                    }), 
                         content_type='application/json')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,{
                                "winners": [
                                    "1",
                                    "2"
                                ]
                            }
                        )   
        # vote ok
        reply = app.put('/doodles/1',data=json.dumps( {
                                                        "person" : "barney",
                                                        "option" : "1"
                                                    }), 
                         content_type='application/json')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,{
                                "winners": [
                                    "1"
                                ]
                            }
                        )  

        #get votes from a person who voted
        reply = app.get('/doodles/1/fred')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,{
                                'votedoptions': 
                                ['1', '2']}
                        )

        #get votes from a person who did not vote
        reply = app.get('/doodles/1/wilma')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,{
                                'votedoptions': 
                                                []}
                        )

        #delete votes from a person who voted
        reply = app.delete('/doodles/1/fred')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,{'removed': True})
        reply = app.get('/doodles/1/fred')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,{'votedoptions':[]})

        #delete votes from a person who did not vote
        reply = app.delete('/doodles/1/wilma')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body,{
                                'removed': False}
                        )

        #get votes from a non-existing poll
        reply = app.get('/doodles/13/fred')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 404)
        self.assertEqual(body,{
                                "code": 404,
                                "description": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",
                                "message": "404 Not Found: The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again."
                            })

        #get votes from a previously existing poll
        reply = app.get('/doodles/2/fred')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(reply.status_code, 410)
        self.assertEqual(body,{
                                "code": 410,
                                "description": "The requested URL is no longer available on this server and there is no forwarding address. If you followed a link from a foreign page, please contact the author of this page.",
                                "message": "410 Gone: The requested URL is no longer available on this server and there is no forwarding address. If you followed a link from a foreign page, please contact the author of this page."
                            })

        

