# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- The UI was clean for a AI game but the game logic was a mess . Certain buttons werent performing its task . There were hidden bugs for sure 
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

- The first concrete bug :   The hints were totally wrong . Example : The range is from 1 to 100 but even if i entered 1 it says to go lower 

- Second Bug is that the hints dont  match and the hints kept changing randomly 

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? 
- Claude 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- The AI sugessted a fix to the game logic which previously shopwed the wrong hint and wrong number . I verified byt testing the AI code and the original code 

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Ran some generated test and live testing 
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  If my guess was 50 and the secret was 60 , it would show too high . This shows that the test is able to perform with zero error

- Did AI help you design or understand any tests? How?
Yes , it showed me what was wrong with some of my written test and explained showed some examples of what my test would have done
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- In the original version, the secret number was probably created with something like random.randint(...) directly in the main flow of the app. In Streamlit, that means every button click, text input, or widget change can trigger a full rerun. So instead of “keeping” the old secret number, the app would generate a brand-new one on each rerun. That makes the game feel broken, because the target changes while the user is guessing.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- Reruns: Streamlit re-executes the entire script whenever the user interacts with the app. Session state: A place to store variables so they persist between reruns during the user’s session.
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- Testing habit . Create few test cases and some edge cases 
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- Not commiting every changes just incase 
- In one or two sentences, describe how this project changed the way you think about AI generated code.
