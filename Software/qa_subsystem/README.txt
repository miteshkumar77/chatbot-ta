'/working/Software/qa_subsystem' contains all code for the Advanced Search
subsystem, and all code for Rule-based Chatbot except the graphical rule tree
editor.

'api.py':
    Combines all Advanced Search and Rule-Based Chatbot methods into a REST API.
    You can test the API by starting the server and visiting the '/docs'
    extension.

'bert_qa.py':
    Provides the following method:

    'answer_question': Used in 'api.py'. Performs a sliding window operation to
        find the answer to a question within a context segment. For the BERT
        model, the context segment must be 512 bytes or smaller.

'build_index.py':
    Provides the following methods:

    'build_content_index': Stores all (url, content) pairs from an input JSON
        file in an SQLite table, where url is a primary key

    'build_keyword_index': Stores all (word_vector, url) pairs from an input
        JSON file in an rtree database (spatially indexed database), where for
        each (wv, u) in the spatial index and (u, c) in the content index, c
        contains a keyword with the word vectorization wv

'get_tasks_dates.py':
    When run as __main__, scrapes the Tasks and Due Dates wiki page
    https://designlab.eng.rpi.edu/edn/projects/capstone-support-dev/wiki/Tasks_and_Due_Dates
    and extracts and saves the assignment and class session data to
    'storage/rules/{class-sessions,assignments,other-dates}.json'.

    TreeSearcher.__init__() (see 'tree_searcher.py') loads the data from these
    files to power the TreeSearcher methods get_assignments() and get_classes(),
    which are currently called from tree_assignments_endpoint() and
    tree_classes_endpoint() in 'api.py' but should be integrated into
    tree_next_endpoint() and the React frontend in the future.

'kwd.py':
    Provides the following methods:

    'get_closest_word_vector': Get the most similar word known by the word2vec
        model

    'get_keywords': Use the Spacy library to extract all nouns and verbs from
        plain text

'preprocess.py':
    Provides the following method:

    'go':
        Summary:
            Fix text formatting on 'EDN scraper' subsystem output. Add 'keyword'
            field of important keywords from the text. Output url -> {context,
            keywords} dictionary as JSON to output file.
        Arguments:
            input_file: Input file name (unmodified)
            output_file: Output file name for cleaned input_file
            output_keyword_file: Output file for keyword to url mapping

'question_answer.py':
    Provides the following method:

    'chatbot_response': apply the 'bert_qa.answer_question' method to the top
        documents ranked by relevance to the user's question, and return the
        best highlighted answer for each document.

'searcher.py':
    Provides the following interface:
        'InvertedIndex':
            'retrieve_relevant_documents':
                given a question, content_index, keyword_index, topn, k:
                retrieve the top 'topn' most relevant documents based on keyword
                similarity using the following approach:

                for each keyword in 'question', find the 'k' nearest keywords
                within the spatial index and retrieve their respective document
                urls. Add these document urls to the sets corresponding to each
                keyword that they were retrieved for. Rank the document urls by
                their frequency among all of these sets. Return the 'topn'
                documents by this ranking.

'tree_searcher.py':
    Provides the following interface:
        'TreeSearcher':
            interface for traversing a tree specified by a rule_spec JSON file.

            'get_node': Get the node associated with a particular id in the rule
                tree

            'get_next_node': Given a current node and a query by the user,
                return the next best node chosen by keyword relevance to the
                user's query

'update_rule_spec.py':
    Provides the following method:
        'build_rule_index': Given a spec_file and an output location, convert
            the spec_file into a compatible format for the 'TreeSearcher'
            interface by converting all keywords to their word vectors, and
            restructuring the tree such that each edge contains the word vectors
            for evaluating that edge's relevance.
