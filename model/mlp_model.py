# https://pytorch.org/tutorials/_images/reinforcement_learning_diagram.jpg	
class MLPModel:
    def __init__(self):
        pass


# Embedding Layer

# def optimize_model():
#     if len(memory) < BATCH_SIZE:
#         return
#     transitions = memory.sample(BATCH_SIZE)
#     # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
#     # detailed explanation). This converts batch-array of Transitions
#     # to Transition of batch-arrays.
#     batch = Transition(*zip(*transitions))

#     # Compute a mask of non-final states and concatenate the batch elements
#     # (a final state would've been the one after which simulation ended)
#     non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
#                                           batch.next_state)), device=device, dtype=torch.bool)
#     non_final_next_states = torch.cat([s for s in batch.next_state
#                                                 if s is not None])
#     state_batch = torch.cat(batch.state)
#     action_batch = torch.cat(batch.action)
#     reward_batch = torch.cat(batch.reward)

#     # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
#     # columns of actions taken. These are the actions which would've been taken
#     # for each batch state according to policy_net
#     state_action_values = policy_net(state_batch).gather(1, action_batch)

#     # Compute V(s_{t+1}) for all next states.
#     # Expected values of actions for non_final_next_states are computed based
#     # on the "older" target_net; selecting their best reward with max(1)[0].
#     # This is merged based on the mask, such that we'll have either the expected
#     # state value or 0 in case the state was final.
#     next_state_values = torch.zeros(BATCH_SIZE, device=device)
#     next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
#     # Compute the expected Q values
#     expected_state_action_values = (next_state_values * GAMMA) + reward_batch

#     # Compute Huber loss
#     criterion = nn.SmoothL1Loss()
#     loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

#     # Optimize the model
#     optimizer.zero_grad()
#     loss.backward()
#     for param in policy_net.parameters():
#         param.grad.data.clamp_(-1, 1)
#     optimizer.step()

#    

# num_inputs = 4
# num_actions = 2
# num_hidden = 128

# inputs = layers.Input(shape=(num_inputs,))
# common = layers.Dense(num_hidden, activation="relu")(inputs)
# action = layers.Dense(num_actions, activation="softmax")(common)
# critic = layers.Dense(1)(common)

# model = keras.Model(inputs=inputs, outputs=[action, critic])

# optimizer = keras.optimizers.Adam(learning_rate=0.01)
# huber_loss = keras.losses.Huber()
# action_probs_history = []
# critic_value_history = []
# rewards_history = []
# running_reward = 0
# episode_count = 0

# while True:  # Run until solved
#     state = env.reset()
#     episode_reward = 0
#     with tf.GradientTape() as tape:
#         for timestep in range(1, max_steps_per_episode):
#             # env.render(); Adding this line would show the attempts
#             # of the agent in a pop up window.

#             state = tf.convert_to_tensor(state)
#             state = tf.expand_dims(state, 0)

#             # Predict action probabilities and estimated future rewards
#             # from environment state
#             action_probs, critic_value = model(state)
#             critic_value_history.append(critic_value[0, 0])

#             # Sample action from action probability distribution
#             action = np.random.choice(num_actions, p=np.squeeze(action_probs))
#             action_probs_history.append(tf.math.log(action_probs[0, action]))

#             # Apply the sampled action in our environment
#             state, reward, done, _ = env.step(action)
#             rewards_history.append(reward)
#             episode_reward += reward

#             if done:
#                 break

#         # Update running reward to check condition for solving
#         running_reward = 0.05 * episode_reward + (1 - 0.05) * running_reward

#         # Calculate expected value from rewards
#         # - At each timestep what was the total reward received after that timestep
#         # - Rewards in the past are discounted by multiplying them with gamma
#         # - These are the labels for our critic
#         returns = []
#         discounted_sum = 0
#         for r in rewards_history[::-1]:
#             discounted_sum = r + gamma * discounted_sum
#             returns.insert(0, discounted_sum)

#         # Normalize
#         returns = np.array(returns)
#         returns = (returns - np.mean(returns)) / (np.std(returns) + eps)
#         returns = returns.tolist()

#         # Calculating loss values to update our network
#         history = zip(action_probs_history, critic_value_history, returns)
#         actor_losses = []
#         critic_losses = []
#         for log_prob, value, ret in history:
#             # At this point in history, the critic estimated that we would get a
#             # total reward = `value` in the future. We took an action with log probability
#             # of `log_prob` and ended up recieving a total reward = `ret`.
#             # The actor must be updated so that it predicts an action that leads to
#             # high rewards (compared to critic's estimate) with high probability.
#             diff = ret - value
#             actor_losses.append(-log_prob * diff)  # actor loss

#             # The critic must be updated so that it predicts a better estimate of
#             # the future rewards.
#             critic_losses.append(
#                 huber_loss(tf.expand_dims(value, 0), tf.expand_dims(ret, 0))
#             )

#         # Backpropagation
#         loss_value = sum(actor_losses) + sum(critic_losses)
#         grads = tape.gradient(loss_value, model.trainable_variables)
#         optimizer.apply_gradients(zip(grads, model.trainable_variables))

#         # Clear the loss and reward history
#         action_probs_history.clear()
#         critic_value_history.clear()
#         rewards_history.clear()

#     # Log details
#     episode_count += 1
#     if episode_count % 10 == 0:
#         template = "running reward: {:.2f} at episode {}"
#         print(template.format(running_reward, episode_count))

#     if running_reward > 195:  # Condition to consider the task solved
#         print("Solved at episode {}!".format(episode_count))
#         break
