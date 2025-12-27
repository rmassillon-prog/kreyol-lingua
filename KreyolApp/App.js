import React, { useState } from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View, ActivityIndicator, Keyboard, ScrollView } from 'react-native';
import axios from 'axios';
import * as Speech from 'expo-speech';

export default function App() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState('');
  const [tokens, setTokens] = useState([]);
  const [loading, setLoading] = useState(false);

  const analyzeText = async () => {
    if (!inputText) return;
    setLoading(true);
    Keyboard.dismiss();
    try {
      const response = await axios.post('https://kreyol-lingua.onrender.com/analyze', { text: inputText });
      setResult(response.data.normalized_text);
      setTokens(response.data.tokens);
    } catch (error) {
      alert("Error connecting to the brain!");
    } finally {
      setLoading(false);
    }
  };

  const speak = () => {
    if (result) {
      Speech.speak(result, { 
        language: 'fr-FR', // Using the Thomas voice you downloaded
        pitch: 0.9,        // Slightly deeper tone
        rate: 0.75         // Slower speed for clarity
      });
    }
  };

  const clearFields = () => { setInputText(''); setResult(''); setTokens([]); };

  const showWordInfo = (token) => {
    const definition = token.tags.find(t => t.startsWith('DEF:'))?.split(':')[1] || 'No definition found';
    const pos = token.tags.find(t => t.startsWith('POS:'))?.split(':')[1] || 'Unknown';
    alert(`Word: ${token.normalized}\nMeaning: ${definition}\nType: ${pos}`);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Kreyòl Lingua</Text>
      <TextInput style={styles.input} placeholder="Type in Kreyòl..." value={inputText} onChangeText={setInputText} multiline />
      <TouchableOpacity style={styles.button} onPress={analyzeText}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Analyze</Text>}
      </TouchableOpacity>
      <TouchableOpacity style={styles.clearButton} onPress={clearFields}><Text style={styles.clearButtonText}>Clear</Text></TouchableOpacity>
      {result ? (
        <View style={styles.resultBox}>
          <Text style={styles.resultLabel}>Normalized Output (Tap words for info):</Text>
          <View style={styles.chipContainer}>
            {tokens.map((token, index) => (
              <TouchableOpacity key={index} onPress={() => showWordInfo(token)}
                style={[styles.wordChip, { backgroundColor: token.original !== token.normalized ? '#fff3cd' : '#fff' }]}>
                <Text style={styles.wordText}>{token.normalized}</Text>
              </TouchableOpacity>
            ))}
          </View>
          <TouchableOpacity style={styles.speakButton} onPress={speak}><Text style={styles.buttonText}>🔊 Listen</Text></TouchableOpacity>
        </View>
      ) : null}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, backgroundColor: '#f5f5f5', alignItems: 'center', justifyContent: 'center', padding: 20 },
  title: { fontSize: 32, fontWeight: 'bold', marginBottom: 20, color: '#003366', marginTop: 40 },
  input: { width: '100%', height: 100, backgroundColor: '#fff', padding: 15, borderRadius: 10, borderColor: '#ccc', borderWidth: 1, textAlignVertical: 'top' },
  button: { backgroundColor: '#003366', padding: 15, borderRadius: 10, marginTop: 20, width: '100%', alignItems: 'center' },
  clearButton: { backgroundColor: '#ccc', padding: 15, borderRadius: 10, marginTop: 10, width: '100%', alignItems: 'center' },
  speakButton: { backgroundColor: '#28a745', padding: 12, borderRadius: 10, marginTop: 20, width: '100%', alignItems: 'center' },
  buttonText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  clearButtonText: { color: '#333', fontSize: 18, fontWeight: 'bold' },
  resultBox: { marginTop: 30, padding: 20, backgroundColor: '#e6f2ff', borderRadius: 10, width: '100%' },
  resultLabel: { fontWeight: 'bold', color: '#003366', marginBottom: 10 },
  chipContainer: { flexDirection: 'row', flexWrap: 'wrap' },
  wordChip: { padding: 8, borderRadius: 8, margin: 4, borderWidth: 1, borderColor: '#bddbff' },
  wordText: { fontSize: 16, color: '#333' }
});
