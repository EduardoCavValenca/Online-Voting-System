from xmlrpc.server import SimpleXMLRPCServer
import json

# Set server configurations
server = SimpleXMLRPCServer(('localhost', 3333), logRequests=True)

# Open json with data
with open('Votes/data.json') as file:
    data = json.load(file)
    file.close()

# Procedures
def getCandidates():
    names = []
    for cand in data["candidates"]:
        names.append(cand["name"])

    return names

def vote(voterCPF, candidate):
    # Verify if voter exits
    voterIndex = 0
    voterExists = False
    for voter in data["voters"]:
        if(voter["CPF"] == voterCPF):       
            voterExists = True
            break    
        voterIndex += 1
    
    # If voter does not exists, then register in database
    if voterExists == False:
        data["voters"].append({"CPF": voterCPF, "didVote": False})
    else:
        # If voter exists, does not allow him to vote twice
        if(data["voters"][voterIndex]["didVote"] == True):
            return "You have already voted!"

    # Voter is registered, then try to vote

    # Check if the candidate exists
    candidateExists = False
    for cand in data["candidates"]:
        if(cand["name"] == candidate):
            # Candidate exists, then register vote
            cand["votes"] += 1
            candidateExists = True
            # Update 'didVote' status of voter
            data["voters"][voterIndex]["didVote"] = True
            break
    

    # Updating json
    if candidateExists == True or voterExists == False:
        with open('Votes/data.json', 'w') as file:
            json.dump(data, file)
        file.close()
    
    # Return messages to the user
    if candidateExists == False:
        return "Invalid candidate"
    else:
        return "Vote added"

# Register procedures
server.register_function(getCandidates)
server.register_function(vote)

if __name__ == '__main__':
    try:
        print('[SERVER] Listening on port 3333...')
        server.serve_forever()
    except KeyboardInterrupt:
        print('[SERVER] Exiting...')
