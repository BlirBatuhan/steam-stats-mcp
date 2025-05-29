import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import ChatBot from './components/ChatBot';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>Steam Analytics Chat Bot</Text>
      </View>
      <ChatBot />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1b2838',
  },
  header: {
    padding: 15,
    backgroundColor: '#171a21',
    borderBottomWidth: 1,
    borderBottomColor: '#2a475e',
  },
  headerText: {
    color: '#66c0f4',
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
  },
});
