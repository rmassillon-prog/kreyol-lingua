import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View, ActivityIndicator, Keyboard, ScrollView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import * as Speech from 'expo-speech';

export default function App() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState('');
  const [tokens, setTokens] = useState([]);
  const [loading, setLoading] = useState(false);
  const [favorites, setFavorites] = useState([]);

  useEffect(() => { loadFavorites(); }, []);

  const loadFavorites = async () => {
    try {
      const saved = await AsyncStorage.getItem('favorites');
      if (saved) setFavorites(JSON.parse(saved));
    } catch (e) { console.log(e); }
  };

  const saveToFavorites = async () => {
    if (!result || favorites.includes(result)) return;
    const newFavs = [result, ...favorites];
    setFavorites(newFavs);
    await AsyncStorage.setItem('favorites', JSON.stringify(newFavs));
  };

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
    } finally { setLoading(false); }
  };

  const speak = (textToSpeak) => {
    // YOUR PHONETIC HACKS
    let phoneticText = textToSpeak.toLowerCase()
      .replace(/\bap\b/g, 'app')
      .replace(/mache/g, 'maché')
      .replace(/manje/g, 'man-zhay')
      .replace(/mwen/g, 'mou-en');

    Speech.speak(phoneticText, { language: 'fr-FR', pitch: 0.9, rate: 0.65 });
  };

  const showWordInfo = (token) => {
    const definition = token.tags.find(t => t.startsWith('DEF:'))?.split(':')[1] || 'No definition found';
    alert(`Word: ${token.normalized}\nMeaning: ${definition}`);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Kreyòl Lingua</Text>
      <TextInput style={styles.input} placeholder="Type..." value={inputText} onChangeText={setInputText} multiline />
      <TouchableOpacity style={styles.button} onPress={analyzeText}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Analyze</Text>}
      </TouchableOpacity>
      
      {result ? (
        <View style={styles.resultBox}>
          <View style={styles.chipContainer}>
            {tokens.map((t, i) => (
              <TouchableOpacity key={i} onPress={() => showWordInfo(t)} style={styles.wordChip}>
                <Text>{t.normalized}</Text>
              </TouchableOpacity>
            ))}
          </View>
          <TouchableOpacity style={styles.speakButton} onPress={() => speak(result)}>
            <Text style={styles.buttonText}>🔊 Listen</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.favButton} onPress={saveToFavorites}>
            <Text style={styles.buttonText}>⭐ Save</Text>
          </TouchableOpacity>
        </View>
      ) : null}

      <View style={styles.favSection}>
        <Text style={styles.favTitle}>Favorites</Text>
        {favorites.map((f, i) => (
          <View key={i} style={styles.favItem}>
            <Text style={{flex: 1}}>{f}</Text>
            <TouchableOpacity onPress={() => speak(f)}><Text>🔊</Text></TouchableOpacity>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, paddingTop: 60 },
  title: { fontSize: 28, fontWeight: 'bold', textAlign: 'center', marginBottom: 20 },
  input: { backgroundColor: '#fff', padding: 15, borderRadius: 10, borderWidth: 1, borderColor: '#ccc' },
  button: { backgroundColor: '#003366', padding: 15, borderRadius: 10, marginTop: 10, alignItems: 'center' },
  buttonText: { color: '#fff', fontWeight: 'bold' },
  resultBox: { marginTop: 20, padding: 15, backgroundColor: '#eef', borderRadius: 10 },
  chipContainer: { flexDirection: 'row', flexWrap: 'wrap' },
  wordChip: { padding: 8, backgroundColor: '#fff', borderRadius: 5, margin: 4, borderWidth: 1, borderColor: '#ccc' },
  speakButton: { backgroundColor: '#28a745', padding: 12, borderRadius: 8, marginTop: 10, alignItems: 'center' },
  favButton: { backgroundColor: '#ffc107', padding: 12, borderRadius: 8, marginTop: 5, alignItems: 'center' },
  favSection: { marginTop: 30 },
  favTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 10 },
  favItem: { backgroundColor: '#fff', padding: 10, borderRadius: 5, marginBottom: 5, flexDirection: 'row' }
});
