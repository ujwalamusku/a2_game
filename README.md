# a2
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 1: Raichu:
Minimax Algorithm with alpha beta pruning : Returns the best move for the automated player.

Approach:
1. We are given an initial board with white pichu and pikachu and black pichu and pikachu. We are expected to find the next move for the defined player so that it wins the game. 
2. So, we first defined functions to calculate the successor states of all the pichus, pikachus and raichus. 
3. Pichu can move only one square diagonally. It can jump over opposite colour pichu diagonally. Pikachu can move 1 or 2 squares forward, left or right and similarly it can jump over piece forward, left or right. Raichu can move any number of squares in any directions. And it can jump over only one piece of opposite colour in any direction.
4. After getting all the successors for the current board, we evaluate the score of the board based on the number of pichus, pikachus and raichu and the number of moves for white and black player. 
5. From the find best move method calls it alpha beta pruning method, which will decide the best next move for the current board based on the score.
6. The method calls the min_value function which calculates the minimum score for the board based on the value returned by the max_value function. The methods cll each other recursively until the max_depth is reached. After the max_depth is reached, the current board's evaluated scored is returned. And based on it we do the further comparisons. 


## Difficulties faced:
1. The problem statement was easy to understand but I faced difficulties in defining the successors function of the boards. Due to this, we were unable to get the desired results out of the raichu game.
2. We took time to discuss it among us again and then defined the moves and jumps part again in brute force manner as the reduced function was giving us error.
3. Next on, I was unclear about what the While True part was doing in the find best move function. Giving considerable amount of time and debugging it, I understood its use and then replaced with the time_limit and is_goal condition and just returned the final board string. 
4. I also had doubt regarding the heuristic funtion used to calculate score of the board. Earlier we used the function which calculates scores based only on the number of pieces of opposite colour on the board. But it was giving us the same output, even if we increase the max_depth limit. Then we added the number of moves available for each player. After that it started giving us different results.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 2: The Game of Quintris:
Genetic Algorithm: Evolving promising states

Approach:
1. We were given a quintris game of 25 rows and 15 columns which should return a string of the possible moves ("b" -> left, "n" -> rotate, "m" -> right, "h" -> horizontal flip). We have two versions given - human and simple. I started with simple version.
2. After going through the existing code (functions to rotate, flip, move left, right and down) and brainstorming with my teammates, I understood that we can reuse the rotate and flip functions to obtain the possible versions of the falling piece. Confirmed the same in the class. For each piece, I'm creating a dictionary that has number of rotations/flip as keys and rotated/flipped verison of the piece as value.
3. Now that I have the initial state in place, I brainstormed with my teammates about the possible heuristics that defines the goodness in a tetris or quintris game. We listed out 4 main heuritics: # of empty gaps that form below an element of the piece("x"), # of rows that have all x's i.e., no empty gap in the row, column heights of each column (i.e., first "x" position from the top in the board for all 15 columns), uneveness of the top part of the board. From these 4 functions, I remember myself trying to avoid making gaps in between, making the tallest block sit on top, and trying to finish off rows by filling rows with all x's. I wrote these heuristic functions in python using the same logic.
4. Now that we have heuristics and possible versions of the falling piece, all we have to do is move the piece left or right based on the above heuristics to form a set of successors. To form the successors and the movements(left/right), I've written two loops that move left and right till it reaches the ends. While moving left/right, I checked if there is any collision with the existing pieces in the board once I drop the piece. If there is a collision, its not a successor and vice-versa. I created a successor list using this logic which saves the movement (rotated/flipped/actual + number of left/right movements) and the dummy board that is obtained after the move is made and dropped in that particular position. 
5. Now that we have successors, we just pass each successor to the heuristic function to obtain gaps, rows formed, column height and uneveness. 
6. Now that we have abstraction in place, we used genetic algorithm. As a first step, I ran 10 games each with one set of random weights (for gaps, rows formed, column height and uneveness to obtain the heuristic score). Later, I ran another 10 games with a new set of random weights, so on. Similarly, I do this for 150 iterations. The top 50% of iteration with high median(to avoid skewness towards min and max score) scores are segregated and the bottom 50% are killed. Using these top 50%, I came up with new children by taking a mean of weights of two parents. Once we have enough population, I ran the whole above process again.This was run for multiple times - 10 times.
7. Finally, I took the set of weights with high median score after 10 final iterations and used these weights in the actual heuristic function.
8. The algorithm returns the movement of the piece of the successor with high heuristic score(assigned negative weights for gaps, height and uneveness and positive weight for rows formed).
9. I observed the range of actual quintris score with a minimum of 15, maximum of 608, average of 91, and a median of 87.

## Difficulties faced:
1. It took quite a while to understand the existing code of Simple and Animated Quintris.
2. The existing right movement function was not letting me to move right till the end and hence this was not giving me all the successors. Because of this, the game was ending soon with zero score. So I debugged in a top to bottom fashion to identify and rectify this. Inorder to rectify this, I've written a code that returns the index with the minimum of piece value column + # of steps and 14(# of columns) and then, I check if there is any collision and if not, its a successor.
3. I faced issues while running multiple games for a certain set of weights. Later I figured out the issue in the loop and reran it.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Part 3: Truth be Told :
Naïve Bayes Classifier: Classification algorithm based on the bayes theorem.
This classifier assumes that each feature is independent of the other features.
# Notes on Part3:
# STEP 1:
Firstly, I have studied both the training and test datasets. The dataset is balanced for both the labels.   
Calculated the probability of each label in the Training dataset:
P(“Truthful”) = no of rows under Truthful label /Total number of rows in the dataset. 
P(“Deceptive”) = no of rows under Deceptive label /Total number of rows in the dataset. 
As the data is balanced, both the labels have same probability. 
# STEP 2:
Applied Data Preprocessing on the Training Data.
1.	Removed the punctuations.
2.	Removed the numbers.
3.	Converting the words to lower case.
# STEP 3: 
Maintained a frequency dictionary to maintain the count of each feature / word respective to each label with key as the word and the value as its count in each label.
# STEP 4:
Applied Laplace smoothing for the test data. The reason for applying this smoothing is because I have observed several words of the test data are not present in the training data or present in either of the training labels but not in both the labels. 
This could lead to errors during the calculation of the probabilities which are used for classification. 
# Approach 1:
For example: the word Damaged in the row 1 of the test data is not present in the training data. So the p (damaged |Truthful) = p (damaged |deceptive) =0
For example: stairs are damaged.
P(stairs are damaged |label)=p(stairs |label)*p(are |label)*p(damaged |label)=0 leads to zero probability
# Approach 2:
Skip or ignore the term i.e., p (damaged |label). But ignoring makes its probability 1 for both labels, which is illogical.
# Approach 3: 
Laplace smoothing adding the alpha in the probability.  This is added to every probabilistic estimate.
# Formula:
# P(x’/positive) = (number of reviews with x’ and target_outcome=positive + α) / (N+ α *k)
Usually, α =1 or any number but not 0.
K is the number of features 
I have applied Laplace smoothing by finding the count of unique words in each row which is K. In each row , for every word , I have checked if the word is in the training data or not , or if the word is in either of the training data label but both for both . and maintained a flag. 
If the word is missing as above that could led to posterior probability becoming 0 . So calculated the probability of each word in that row with the above Laplace smoothing formula with alpha =1 and k =len(unique words in row .)
If the word is present in the training data for both the labels:
P (word |label)= frequency[word][label_1]/count[label_1] 
# Step 5:
Applied log on each probability to improve the accuracy 
On multiplying each probability which are small , the result becomes much smaller and accuracy reduces .
prob_row_label_1=prob_row_label_1+ math.log(frequency[word][label_1]/count[label_1])
prob_row_label_2=prob_row_label_2+math.log(frequency[word][label_2]/count[label_2])
 
# Step 6:
On applying the log of probabilities on each label, check which is greater and update its label to the list and return it . 
In the main function, this estimated list of labels are checked with the test labels and accuracy is calculated for our naïve bayes classification. 
The observed accuracy for the given data set is 82.50% 

Interestingly, I have observed that before removing the punctuations, numbers, applying Laplace smoothing , accuracy of 85 % is achieved. 
But on applying the data preprocessing steps and Laplace smoothing, the accuracy reduced to 82.50 % . This is because removing punctuations, numbers and converting them to lower case  has reduced the number of words for each label differs. 
As most of the reviews contain the words that are not present in the training data . On applying Laplace smoothing, the accuracy is different after applying it . 

On applying stop words , the accuracy increased to 83% which was not much .I took a list of stop words and checked if the word is in the stop word list , to continue to the next word . I was doubtful on how to take the stop words if the language defers the stop words change and we cant as use NLTK package .  

