from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def classifyMessages(DataMessage, DataMessageAll):
	category_size = len(DataMessage)
	DataMessageGroup = [[elem] for elem in DataMessage]
	MessageClassified = [0 for elem in DataMessageAll]

	for elem in DataMessageAll:
		DataMessage.append(elem)

	model = SentenceTransformer('bert-base-nli-mean-tokens')
	encoded_messages = model.encode(DataMessage)

	for i in range(category_size):
		word_similarities = cosine_similarity([encoded_messages[i]], encoded_messages[category_size:])
		index = 0
		for elem in word_similarities[0]:
			if elem > 0.75:
				print(elem)
				DataMessageGroup[i].append(DataMessageAll[index])
				MessageClassified[index] = 1
		index += 1

	for i in range(len(MessageClassified)):
		if not MessageClassified[i]:
			DataMessageGroup.append([DataMessageAll[i]])

	print(DataMessageGroup)
	return DataMessageGroup
        
