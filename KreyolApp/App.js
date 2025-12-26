import React, { useState } from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View, ActivityIndicator, Keyboard } from 'react-native';
import axios from 'axios';

export default function App() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const analyzeText = async () => {
    if (!inputText) return;
    setLoading(true);
    Keyboard.dismiss();

    try {
      // Connects to your live engine on Render
      const response = await axios.post('https://kreyol-lingua.onrender.com/analyze', {
        text: inputText
      });
      
      setResult(response.data.normalized_text);
    } catch (error) {
      alert("Error connecting to the brain!");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Kreyòl Lingua</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Type in Kreyòl (e.g., M'ap manje...)"
        value={inputText}
        onChangeText={setInputText}
        multiline
      />

      <TouchableOpacity style={styles.button} onPress={analyzeText}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Analyze</Text>}
      </TouchableOpacity>

      {result ? (
        <View style={styles.resultBox}>
          <Text style={styles.resultLabel}>Normalized Output:</Text>
          <Text style={styles.resultText}>{result}</Text>
        </View>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5', alignItems: 'center', justifyContent: 'center', padding: 20 },
  title: { fontSize: 32, fontWeight: 'bold', marginBottom: 40, color: '#003366' },
  input: { width: '100%', height: 100, backgroundColor: '#fff', padding: 15, borderRadius: 10, borderColor: '#ccc', borderWidth: 1, textAlignVertical: 'top' },
  button: { backgroundColor: '#003366', padding: 15, borderRadius: 10, marginTop: 20, width: '100%', alignItems: 'center' },
  buttonText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  resultBox: { marginTop: 40, padding: 20, backgroundColor: '#e6f2ff', borderRadius: 10, width: '100%' },
  resultLabel: { fontWeight: 'bold', color: '#003366', marginBottom: 5 },
  resultText: { fontSize: 18, color: '#333' }
});
