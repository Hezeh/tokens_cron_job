from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import datetime
import os

# project_id = os.environ.get('PROJECT_ID')

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'beammart',
})

db = firestore.client()

app = FastAPI()

@app.post('/')
async def main():
    items_ref = db.collection(u'items')
    docs = items_ref.stream()
    for doc in docs:
        # print(f'{doc.id} => {doc.to_dict()}')
        data = doc.to_dict()
        if 'lastRenewal' in data:
            lastRenewal = data['lastRenewal']

            if 'userId' in data:
                merchantId = data['userId']
                if 'category' in data:
                    category = data['category']
                    timestamp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(lastRenewal, '%Y-%m-%dT%H:%M:%S.%f')))
                    renewalTime = datetime.datetime.now() - datetime.timedelta(days=7)
                    # Should be less than
                    if timestamp < renewalTime:
                        # Get the tokens for this specific user
                        tokensBalance = get_tokens(merchantId)
                        # Get the tokens needed
                        tokensRequired = get_category_tokens(category)
                        # Check if the tokens are enough
                        if tokensBalance > tokensRequired:
                            print("Checking if user has required tokens")
                            # Bill the client
                            # Update the status to active & lastRenewal to current timestamp
                            docRef = db.collection(u'items').document(f'{doc.id}')
                            docRef.set({
                                'lastRenewal': datetime.datetime.now().isoformat(),
                                'isActive': True,
                            }, merge=True)
                            # Set new number of tokens
                            newTokensBalance = tokensBalance - tokensRequired
                            db.collection(u'profile').document(merchantId).set({
                                'tokensBalance': newTokensBalance
                            }, merge=True)
                        else:
                            # TODO If not enough tokens, send an email & notification to client 
                            # to let them know the don't have enough tokens/buy more tokens.
                            doc.set({
                                'isActive': False
                            }, merge=True)
                            return
                    else:
                        return
    return {}

def get_tokens(userId):
    merchant_doc = db.collection(u'profile').document(userId).get()
    if merchant_doc.exists:
        # Get the current tokens balance
        print(merchant_doc.to_dict())
        dict_doc = merchant_doc.to_dict()
        tokensBalance = dict_doc['tokensBalance']
        return tokensBalance
    else:
        # Just return 0
        print("Document does not exist")
        return 0

def get_category_tokens(category):
    tokens_doc = db.collection(u'tokens').document('categories').get()
    if tokens_doc.exists:
        print(tokens_doc.to_dict())
        data = tokens_doc.to_dict()
        # Check if the field is available
        if category == 'Electronics' and data['electronicsTokens'] != None:
            return data['electronicsTokens']
        elif category == 'Arts and Crafts' and data['artCraftTokens'] != None:
            return data['artCraftTokens']
        elif category == 'Automotive' and data['automotiveTokens'] != None:
            return data['automotiveTokens']
        elif category == 'Baby' and data['babyTokens'] != None:
            return data['']
        elif category == 'Beauty and Personal Care' and data['beautyPersonalCareTokens'] != None:
            return data['beautyPersonalCareTokens']
        elif category == 'Computers' and data['computersTokens'] != None:
            return data['computersTokens']
        elif category == 'Food' and data['foodTokens'] != None:
            return data['foodTokens']
        elif category == 'Health and Household' and data['healthHouseholdTokens'] != None:
            return data['healthHouseholdTokens']
        elif category == 'Home and Kitchen' and data['homeKitchenTokens'] != None:
            return data['homeKitchenTokens']
        elif category == 'Household Essentials' and data['householdEssentialsTokens'] != None:
            return data['householdEssentialsTokens']
        elif category == 'Industrial and Scientific' and data['industrialScientificTokens'] != None:
            return data['industrialScientificTokens']
        elif category == 'Luggage' and data['luggageTokens'] != None:
            return data['luggageTokens']
        elif category == "Men's Fashion" and data['mensFashionTokens'] != None:
            return data['mensFashionTokens']
        elif category == 'Patio and Garden' and data['patioGardenTokens'] != None:
            return data['patioGardenTokens']
        elif category == 'Pet Supplies' and data['petSuppliesTokens'] != None:
            return data['petSuppliesTokens']
        elif category == 'Smart Home' and data['smartHomeTokens'] != None:
            return data['smartHomeTokens']
        elif category == 'Sports, Fitness and Outdoors' and data['sportsFitnessOutdoorsTokens'] != None:
            return data['sportsFitnessOutdoorsTokens']
        elif category == 'Tools and Home Improvement' and data['toolsHomeImprovementTokens'] != None:
            return data['toolsHomeImprovementTokens']
        elif category == 'Toys and Games' and data['toysGamesTokens'] != None:
            return data['toysGamesTokens']
        elif category == "Women's Fashion" and data['womensFashionTokens'] != None:
            return data['womensFashionTokens']
        else:
            return 10
    else:
        print("Document does not exist")
        return 0