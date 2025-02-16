# from flask import Flask, jsonify
# from flask_cors import CORS  # Import CORS
# import requests
# import os


# app = Flask(__name__)

# CORS(app)


# #GITHUB_TOKEN = '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'
# GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


# GITHUB_API_BASE_URL = 'https://api.github.com'
# GITHUB_GRAPHQL_URL = 'https://api.github.com/graphql'

# def get_contributions(username, repo_name, token):
   
#     repo_url = f'{GITHUB_API_BASE_URL}/repos/{username}/{repo_name}'
#     headers = {'Authorization': f'token {token}'}
#     repo_response = requests.get(repo_url, headers=headers)
#     repo_data = repo_response.json()

#     # Fetch pull requests using GraphQL
#     query = '''
#     query {
#       repository(owner: "%s", name: "%s") {
#         pullRequests(first: 100) {
#           nodes {
#             additions
#             deletions
#             changedFiles
#             author {
#               login
#             }
#             reviews(first: 100) {
#               nodes {
#                 author {
#                   login
#                 }
#               }
#             }
#           }
#         }
#       }
#     }
#     ''' % (username, repo_name)

#     graphql_response = requests.post(GITHUB_GRAPHQL_URL, headers=headers, json={'query': query})
#     graphql_data = graphql_response.json()

#     contributions = {
#         'created_prs': {},
#         'reviewed_prs': {},
#         'users': {}
#     }

    
#     for pr in graphql_data['data']['repository']['pullRequests']['nodes']:
#         contributor = pr['author']['login']

        
#         if contributor not in contributions['users']:
#             contributions['users'][contributor] = {
#                 'file_changes': 0,
#                 'line_changes': 0,
#                 'prs': 0
#             }

#         contributions['users'][contributor]['file_changes'] += pr['changedFiles']
#         contributions['users'][contributor]['line_changes'] += pr['additions'] + pr['deletions']
#         contributions['users'][contributor]['prs'] += 1

        
#         if contributor in contributions['created_prs']:
#             contributions['created_prs'][contributor] += 1
#         else:
#             contributions['created_prs'][contributor] = 1

        
#         for review in pr['reviews']['nodes']:
#             reviewer = review['author']['login']
#             if reviewer in contributions['reviewed_prs']:
#                 contributions['reviewed_prs'][reviewer] += 1
#             else:
#                 contributions['reviewed_prs'][reviewer] = 1

#     return contributions

# @app.route('/get_contributions/sample-collab')
# def get_sample_collab_contributions():
#     username = 'sample-collab'
#     repo_name = 'sample-collab'
#     contributions = get_contributions(username, repo_name, GITHUB_TOKEN)
#     return jsonify(contributions)

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)


from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set. Please add it to your environment variables.")

GITHUB_API_BASE_URL = 'https://api.github.com'
GITHUB_GRAPHQL_URL = 'https://api.github.com/graphql'

def get_contributions(username, repo_name, token):
    headers = {'Authorization': f'token {token}'}
    
    query = '''
    query {
      repository(owner: "%s", name: "%s") {
        pullRequests(first: 100) {
          nodes {
            additions
            deletions
            changedFiles
            author { login }
            reviews(first: 100) {
              nodes { author { login } }
            }
          }
        }
      }
    }''' % (username, repo_name)

    graphql_response = requests.post(GITHUB_GRAPHQL_URL, headers=headers, json={'query': query})
    graphql_data = graphql_response.json()

    print(graphql_data)  # Log the response for debugging

    if 'message' in graphql_data and graphql_data['message'] == 'Bad credentials':
        return {'error': 'Invalid GitHub token. Please check your token permissions.'}

    if 'data' not in graphql_data:
        return {'error': graphql_data.get('message', 'Failed to fetch data')}

    contributions = {'created_prs': {}, 'reviewed_prs': {}, 'users': {}}

    for pr in graphql_data['data']['repository']['pullRequests']['nodes']:
        contributor = pr['author']['login']
        if contributor not in contributions['users']:
            contributions['users'][contributor] = {'file_changes': 0, 'line_changes': 0, 'prs': 0}
        contributions['users'][contributor]['file_changes'] += pr['changedFiles']
        contributions['users'][contributor]['line_changes'] += pr['additions'] + pr['deletions']
        contributions['users'][contributor]['prs'] += 1
        if contributor in contributions['created_prs']:
            contributions['created_prs'][contributor] += 1
        else:
            contributions['created_prs'][contributor] = 1
        for review in pr['reviews']['nodes']:
            reviewer = review['author']['login']
            if reviewer in contributions['reviewed_prs']:
                contributions['reviewed_prs'][reviewer] += 1
            else:
                contributions['reviewed_prs'][reviewer] = 1

    return contributions

@app.route('/get_contributions/sample-collab')
def get_sample_collab_contributions():
    username = 'sample-collab'
    repo_name = 'sample-collab'
    contributions = get_contributions(username, repo_name, GITHUB_TOKEN)
    return jsonify(contributions)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


