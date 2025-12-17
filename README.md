1. Intro
The Github holds a program for a Food Waste App! The app's goal is to connect local food businesses that want to sell their food waste inventory to hungry customers looking for their favorite meals at a discount. By turning potential waste into "Surprise Bags," we help the environment, reduce the food that buisnesses throw away, and satisfy the community.


2. Problem
The Challenge of having a Surplus of food Every day is that the amount tends to be unpredictable. As a result, perfectly good food is thrown away because businesses cannot accurately predict daily demand.

- The Business Problem: Stores lose revenue on unsold inventory.

- The Environmental Problem: Food waste contributes significantly to global CO2 emissions.

- The Satisfaction Problem: recomending many customers will leave some customers dissatisfied, ruining their trust in the food buisness and the app.

- As a solution, An algorithm will be made to find the best local optimal solution.



3. Our Program
The project is built as a modular simulation environment to test different marketplace strategies.

- Simulator:
  The engine that runs daily cycles, manages customer behavior, and tracks inventory across multiple days.

- The Store & Customer Objects: Data models that track location (Lat/Long), ratings, and personalized valuations.

- The Algorithm Suite: A collection of different recommendation strategies:

   * Greedy Baseline: A simple "top-rated" sorter.

   * The one big algorithm that we are still working on

 
4. Development of the Main algorithm

- Done by having all 4 members brainstorm and write 4 algorithms that best solve the problem

  * running the 4 algorithms through the same simulation

  * Using the results/data, run through a graph

  * Select the 2 best algorithms accordding to Revenue effecency, then combine them into one algirihtm


5. Solution

The final algorithm brings together personalization, general quality, and exploration into one balanced decision-making process. It prioritizes stores that the customer has previously enjoyed, while still considering important practical factors such as price, rating, distance, and availability. At the same time, it deliberately introduces new or unfamiliar stores so the recommendations do not become repetitive or overly biased toward past behavior. By scoring all available stores using this combined perspective and selecting the highest-ranked ones, the algorithm ensures that recommendations remain relevant, fair, and adaptable to different users and situations.  

