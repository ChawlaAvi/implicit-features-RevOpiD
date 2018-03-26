run:

	python3 1check.py
	python3 2obtain_cleandata.py
	
	python3 3mining_opinion_features.py
	python3 4words_to_num.py
	cp num_phrase.txt CBA/num_phrase.txt
	cd CBA;\
	javac *.java;\
	java ClassCBA_App -Fnum_phrase.txt -N1 -C50 -S0.5 > output.txt
	cd ..;\
	pwd
	cp ./CBA/output.txt ./output.txt
	python3 5num_to_words.py
	python3 6compactness_pruning.py
	python3 7redundancy_pruning.py
	python3 8opinion_words_extraction.py 
	python3 9orientation_identification_opinion_words.py

	python3 10select_nouns.py 

	python3 11produce_matrix_M_part0.py
	python3 12produce_matrix_M_part1.py
	python3 13tillnow_part1.py	
	python3 14produce_matrix_M_part2.py
	python3 15tillnow_part2.py	
	python3 16remove_feature_from_M.py
	python3 17remove_opinion_from_M.py
	python3 18tillnow_part3.py
	python3 19sentence_wise_mapping_of_M.py
	python3 20sentences_with_no_explicit_features.py
	python3 21count_of_all_notional_words.py
	python3 22find_notional_words.py
	python3 23produce_matrix_C.py
	python3 24find_candidate_features.py    #check the minimum links an opinion must have with a feature. 
	python3 25extract_submatrix_from_C.py 
	python3 26final_matrix_after_including_implicit.py
	python3 27makecsv.py

