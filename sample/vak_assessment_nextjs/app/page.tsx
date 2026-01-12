'use client';

import { useState, useEffect } from 'react';
import { VAK_QUESTIONS, calculateScores, getDominantType } from '@/lib/vakData';
import QuestionView from '@/components/QuestionView';
import ResultView from '@/components/ResultView';

export default function Home() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [completed, setCompleted] = useState(false);

  // 結果表示時に画面トップへスクロール
  useEffect(() => {
    if (completed) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, [completed]);

  const handleAnswer = (questionId: number, score: number) => {
    setAnswers(prev => ({ ...prev, [questionId]: score }));
    
    if (currentQuestion < VAK_QUESTIONS.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setCompleted(true);
    }
  };

  const handleBack = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleRestart = () => {
    setCurrentQuestion(0);
    setAnswers({});
    setCompleted(false);
  };

  if (completed) {
    const scores = calculateScores(answers);
    const dominantType = getDominantType(scores);
    
    return (
      <ResultView 
        scores={scores} 
        dominantType={dominantType}
        onRestart={handleRestart}
      />
    );
  }

  return (
    <QuestionView
      currentQuestion={currentQuestion}
      totalQuestions={VAK_QUESTIONS.length}
      question={VAK_QUESTIONS[currentQuestion]}
      onAnswer={handleAnswer}
      onBack={handleBack}
      canGoBack={currentQuestion > 0}
    />
  );
}
