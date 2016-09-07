#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, json

def detect_fake_user(user):
	req_for_friendsAmount = requests.get("https://graph.facebook.com/v2.5/{0}/friends?access_token={1}".format(user['from']['id'], token))
	friends_json = json.loads(req_for_friendsAmount.text)
	try:
		print(friends_json)
		if friends_json['summary']['total_count']<200:
			print(user['from']['name'], '朋友數小於200')
		else:
			print(user['from']['name'], '是真的帳號')
	except Exception as e:
		r = requests.get("https://graph.facebook.com/v2.5/{0}/?access_token={1}".format(user['from']['id'], token))
		fj=json.loads(r.text)
		print(fj['name'], '這個表子不讓你爬好友喔')

def parse_comment(i, token):
	req_for_posts = requests.get("https://graph.facebook.com/v2.5/{0}/comments?access_token={1}".format(i['id'], token))# api用post就會顯示該使用者的貼文的ID再加上comments就會顯示該篇貼文的評論
	postJson = json.loads(req_for_posts.text)
	# print(postJson)
	for j in postJson['data']:
		# print(j)
		req_for_comments = requests.get("https://graph.facebook.com/v2.5/{0}/comments?access_token={1}".format(j['id'], token))#用該篇評論的id再接comments就會顯示該則回應底下的所有回應
		commentJson = json.loads(req_for_comments.text)
		for k in commentJson['data']:
			# print(k)
			detect_fake_user(k)


def parse_post(token):
	re = requests.get('https://graph.facebook.com/v2.5/tsaiingwen/posts?limit=1&access_token=' + token)# api用post就會顯示該使用者的貼文s
	#if you want to chose a specific time span, append 'since=1420041600' after 'post?' 
	#cause it use Unix seconds, so 1420041600 means 2015/01/01
	jsonObj=json.loads(re.text)		
	for i in jsonObj['data']:
		parse_comment(i, token)

if __name__  ==  "__main__":
	with open('accessToken.txt','r',encoding='utf-8') as f:
		token = f.read()
	parse_post(token)