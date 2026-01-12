import { VAKQuestion } from '@/lib/vakData';

interface QuestionViewProps {
  currentQuestion: number;
  totalQuestions: number;
  question: VAKQuestion;
  onAnswer: (questionId: number, score: number) => void;
  onBack: () => void;
  canGoBack: boolean;
}

export default function QuestionView({
  currentQuestion,
  totalQuestions,
  question,
  onAnswer,
  onBack,
  canGoBack,
}: QuestionViewProps) {
  const progress = ((currentQuestion + 1) / totalQuestions) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* ヘッダー */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
            🎯 コミュニケーションタイプ診断
          </h1>
          <p className="text-gray-600">あなたの強みを活かそう！</p>
        </div>

        {/* 進捗 */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">
              質問 {currentQuestion + 1} / {totalQuestions}
            </span>
            <span className="text-sm font-medium text-primary">
              {Math.round(progress)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-primary h-3 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* 質問カード */}
        <div className="bg-white rounded-lg shadow-xl p-8 mb-6">
          <h2 className="text-xl md:text-2xl font-semibold text-gray-800 mb-8 leading-relaxed">
            {question.question}
          </h2>

          {/* 回答ボタン */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
            {[
              { score: 1, label: '全く当てはまらない' },
              { score: 2, label: 'やや当てはまらない' },
              { score: 3, label: 'どちらとも言えない' },
              { score: 4, label: 'やや当てはまる' },
              { score: 5, label: 'とても当てはまる' },
            ].map(({ score, label }) => (
              <button
                key={score}
                onClick={() => onAnswer(question.id, score)}
                className="bg-primary hover:bg-blue-600 text-white font-medium py-4 px-6 rounded-lg transition-all duration-200 hover:scale-105 active:scale-95 shadow-md hover:shadow-lg"
              >
                <div className="text-sm mb-1">{label}</div>
                <div className="text-2xl font-bold">{score}</div>
              </button>
            ))}
          </div>
        </div>

        {/* 戻るボタン */}
        {canGoBack && (
          <div className="text-center">
            <button
              onClick={onBack}
              className="text-gray-600 hover:text-gray-800 font-medium py-2 px-6 rounded-lg hover:bg-white transition-all duration-200"
            >
              ⬅️ 前の質問に戻る
            </button>
          </div>
        )}

        {/* サイドバー情報 */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📋 診断について</h3>
          <div className="space-y-3 text-sm text-gray-700">
            <div>
              <span className="font-semibold">V - Visual（視覚型）</span>
              <p className="text-gray-600">見た目や資料から情報を得るのが得意</p>
            </div>
            <div>
              <span className="font-semibold">A - Auditory（聴覚型）</span>
              <p className="text-gray-600">会話や説明を通じて理解するのが得意</p>
            </div>
            <div>
              <span className="font-semibold">K - Kinesthetic（体感覚型）</span>
              <p className="text-gray-600">体験や実践を通じて理解するのが得意</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
