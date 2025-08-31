# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title='BB84 Simulator', layout='wide')
st.title('🔑 BB84 Quantum Key Distribution Simulator')
st.write('Simulate sender, receiver, and eavesdropper interactions with visual feedback!')

# ====== User Inputs ======
num_qubits = st.sidebar.slider('Number of Qubits', 10, 50, 20)
attack_mode = st.sidebar.selectbox('Eavesdropper Attack?', ['No', 'Yes'])

# ====== Step 1: Sender generates bits and bases ======
sender_bits = np.random.randint(0, 2, num_qubits)
sender_bases = np.random.choice(['+', 'x'], num_qubits)

# ====== Step 2: Receiver chooses bases and measures ======
receiver_bases = np.random.choice(['+', 'x'], num_qubits)
receiver_bits = []
disturbance = []

for s_bit, s_base, r_base in zip(sender_bits, sender_bases, receiver_bases):
    # Eve attack
    if attack_mode == 'Yes':
        eve_base = np.random.choice(['+', 'x'])
        if eve_base != s_base:
            disturbance.append(1)
        else:
            disturbance.append(0)
    else:
        disturbance.append(0)
        
    # Receiver measurement
    if s_base == r_base:
        receiver_bits.append(s_bit)
    else:
        receiver_bits.append(np.random.randint(0,2))

sender_bits = np.array(sender_bits)
receiver_bits = np.array(receiver_bits)
disturbance = np.array(disturbance)

# ====== Step 3: Key Sifting (Comparer) ======
matching_indices = np.where(sender_bases == receiver_bases)[0]
key_sender = sender_bits[matching_indices]
key_receiver = receiver_bits[matching_indices]

# ====== Step 4: Scoreboard ======
secure_bits = len(key_sender) - sum(disturbance[matching_indices])
attacked_bits = sum(disturbance[matching_indices])

st.subheader('🎯 Scoreboard')
st.write(f"✅ Secure Bits Kept: {secure_bits}")
st.write(f"⚠️ Bits Lost to Attack: {attacked_bits}")

# ====== Step 5: Real-time Qubit Visual ======
st.subheader('🎨 Qubit Visuals')
fig, ax = plt.subplots(figsize=(12,2))
colors = ['green' if d==0 else 'red' for d in disturbance]
ax.bar(range(num_qubits), [1]*num_qubits, color=colors)
ax.set_xticks(range(num_qubits))
ax.set_xticklabels([f'{b}\n{s}' for b,s in zip(sender_bases,sender_bits)])
ax.set_yticks([])
st.pyplot(fig)

# ====== Step 6: Secret Chat ======
st.subheader('💬 Secret Chat (Encrypted with QKD Key)')
chat_input = st.text_input('Enter message to send:')

if st.button('Send'):
    if len(key_sender) == 0:
        st.warning("No secure key established! Run simulation first.")
    else:
        # XOR encryption with key
        key_for_message = key_sender[:len(chat_input)]
        encrypted = ''.join([str(int(c)^k) for c,k in zip(map(int,map(str,chat_input)), key_for_message)])
        st.write(f"Encrypted Message: {encrypted}")
        decrypted = ''.join([str(int(e)^k) for e,k in zip(encrypted,key_for_message)])
        st.write(f"Decrypted Message: {decrypted}")