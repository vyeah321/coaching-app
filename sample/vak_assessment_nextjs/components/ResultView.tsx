'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';
import { VAKScores, getTypeName, TYPE_INFO, getTypeClosing } from '@/lib/vakData';

// Plotlyを動的インポート（SSR無効化）
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

interface ResultViewProps {
  scores: VAKScores;
  dominantType: 'V' | 'A' | 'K' | 'balanced';
  onRestart: () => void;
}

export default function ResultView({ scores, dominantType, onRestart }: ResultViewProps) {
  const [email, setEmail] = useState('');

  const generateEmailBody = () => {
    const typeName = getTypeName(dominantType);
    const closing = getTypeClosing(dominantType);
    
    let advice = '';
    if (dominantType === 'balanced') {
      advice = `あなたは「バランス型」です！

状況に応じて柔軟にコミュニケーションスタイルを変えられる才能があります。
視覚、聴覚、体感覚のすべてをバランスよく使えるため、
相手のタイプに合わせた効果的なアプローチが可能です。

【この特性を活かせる場面】
• ビジネスの商談や提案：相手に合わせて柔軟に対応
• ワイン会などの社交の場：様々なタイプの人と良好な関係を築く
• チームマネジメント：メンバーの個性に合わせた指導

${closing}`;
    } else {
      const typeInfo = TYPE_INFO[dominantType];
      advice = `あなたは「${typeInfo.title}」優勢型です！

${typeInfo.description}

【強み】
${typeInfo.strengths.map(s => `• ${s}`).join('\n')}

この強みを活かしながら、他のタイプも意識することで、
より幅広い人との効果的なコミュニケーションが可能になります。

【ビジネスシーンでの活用】
• 自分の強みを活かした提案スタイルの確立
• 相手のタイプを見極めて、アプローチを調整
• チームの多様性を理解し、効果的に協働

${closing}`;
    }

    return `━━━━━━━━━━━━━━━━━━━━━━
【あなたのコミュニケーションタイプ診断結果】
━━━━━━━━━━━━━━━━━━━━━━

こんにちは！

先ほどの診断、お疲れ様でした。
あなたの結果をお届けします。

━━━━━━━━━━━━━━━━━━━━━━
📊 あなたのスコア
━━━━━━━━━━━━━━━━━━━━━━

${typeName}

👀 見るタイプ（視覚型）: ${scores.V}/20点
👂 聞くタイプ（聴覚型）: ${scores.A}/20点
✋ 体感タイプ（体感覚型）: ${scores.K}/20点

━━━━━━━━━━━━━━━━━━━━━━
💡 あなたのタイプの活かし方
━━━━━━━━━━━━━━━━━━━━━━

${advice}

━━━━━━━━━━━━━━━━━━━━━━
🌟 この力をもっと伸ばしたい方へ
━━━━━━━━━━━━━━━━━━━━━━

自分のタイプを知ることは第一歩。

次は、「相手の可能性を引き出す力」を
身につけてみませんか？

✅ 部下が自ら考え動く、自走するチーム
✅ お客様の本当のニーズを引き出す
✅ 初対面でも深い信頼関係を築ける

30年以上の実績を持つプロから学べます。

詳しくはこちら 👇
https://pro-coach.net/p/r/8uCeXl3l?free20=0030005

━━━━━━━━━━━━━━━━━━━━━━

今日のワイン会、楽しんでくださいね🍷

VAK コミュニケーションタイプ診断より`;
  };

  const handleEmailSend = () => {
    if (!email.includes('@')) return;
    
    const subject = '【診断結果】あなたのコミュニケーションタイプ';
    const body = generateEmailBody();
    const mailto = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = mailto;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* ヘッダー */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">🎉 診断完了！</h1>
          <p className="text-gray-600">あなたの結果はこちらです</p>
        </div>

        {/* レーダーチャート */}
        <div className="bg-white rounded-lg shadow-xl p-6 mb-6">
          <Plot
            data={[
              {
                type: 'scatterpolar',
                r: [scores.V, scores.A, scores.K],
                theta: ['Visual<br>視覚型', 'Auditory<br>聴覚型', 'Kinesthetic<br>体感覚型'],
                fill: 'toself',
                line: { color: 'rgb(99, 110, 250)', width: 3 },
                fillcolor: 'rgba(99, 110, 250, 0.3)',
              },
            ]}
            layout={{
              autosize: true,
              polar: {
                radialaxis: {
                  visible: true,
                  range: [0, 20],
                  automargin: true,
                  tickfont: { size: 11 },
                },
                angularaxis: {
                  tickfont: { size: 12 },
                  automargin: true,
                },
              },
                  showlegend: false,
                  height: 440,
                  /* 上にタイトル領域を確保して、下の余白は小さくする */
                  margin: { t: 40, b: 12, l: 60, r: 60 },
                  title: {
                    text: 'スコア分布',
                    font: { size: 20 },
                    x: 0.5,
                    xanchor: 'center',
                    y: 0.98,
                    yanchor: 'top',
                    pad: { t: 6, b: 0 },
                  },
            }}
            config={{ staticPlot: true, displayModeBar: false }}
            style={{ width: '100%' }}
          />
        </div>

        {/* スコア表示 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {[
            { type: 'V', label: '👀 見るタイプ', score: scores.V },
            { type: 'A', label: '👂 聞くタイプ', score: scores.A },
            { type: 'K', label: '✋ 体感タイプ', score: scores.K },
          ].map(({ type, label, score }) => (
            <div key={type} className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-center mb-3">
                <div className="text-sm text-gray-600 mb-1">{label}</div>
                <div className="text-3xl font-bold text-primary">{score}/20</div>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-primary h-3 rounded-full transition-all duration-300"
                  style={{ width: `${(score / 20) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* タイプ表示 */}
        <div className="bg-white rounded-lg shadow-xl p-6 mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">🌟 あなたのコミュニケーションタイプ</h2>
          <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
            <p className="text-xl font-semibold text-green-800">{getTypeName(dominantType)}</p>
          </div>
        </div>

        {/* タイプ別アドバイス - 続く */}
        {dominantType === 'balanced' ? (
          <div className="bg-blue-50 rounded-lg shadow-lg p-6 mb-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">💡 あなたのタイプの活かし方</h3>
            <div className="space-y-4 text-gray-700">
              <p className="font-semibold text-lg">バランス型：あらゆる場面に対応できる才能</p>
              <p>
                あなたは状況に応じて柔軟にコミュニケーションスタイルを変えられる才能があります！
                視覚、聴覚、体感覚のすべてをバランスよく使えるため、
                相手のタイプに合わせた効果的なアプローチが可能です。
              </p>
              <div>
                <p className="font-semibold">ビジネスシーンでの活用</p>
                <ul className="list-disc list-inside ml-4 mt-2">
                  <li>相手のタイプに合わせて柔軟に対応</li>
                  <li>視覚資料・対話・実践を組み合わせた提案</li>
                  <li>多様なチームメンバーとの効果的な協働</li>
                </ul>
              </div>
              <div>
                <p className="font-semibold">人間関係での活用</p>
                <ul className="list-disc list-inside ml-4 mt-2">
                  <li>ワイン会では、様々なタイプの人と良好な関係を築く</li>
                  <li>相手の反応を見ながら最適なアプローチを選択</li>
                  <li>どんな場面でも柔軟に対応できる</li>
                </ul>
              </div>
              <p className="font-semibold text-primary">{getTypeClosing(dominantType)}</p>
            </div>
          </div>
        ) : (
          <div className="bg-blue-50 rounded-lg shadow-lg p-6 mb-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">💡 あなたのタイプの活かし方</h3>
            <div className="space-y-4 text-gray-700">
              <p className="font-semibold text-lg">{TYPE_INFO[dominantType].title} 優勢型</p>
              <p>
                あなたは特に{TYPE_INFO[dominantType].title}の特徴が強く表れています。
                この強みを活かしながら、他のタイプも意識することで、
                より幅広い人との効果的なコミュニケーションが可能になります。
              </p>
              <div>
                <p className="font-semibold">ビジネスシーンでの活用</p>
                <ul className="list-disc list-inside ml-4 mt-2">
                  {TYPE_INFO[dominantType].businessTips.map((tip, i) => (
                    <li key={i}>{tip}</li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="font-semibold">人間関係での活用</p>
                <ul className="list-disc list-inside ml-4 mt-2">
                  <li>ワイン会では、{TYPE_INFO[dominantType].wineTips.join('、')}</li>
                </ul>
              </div>
              <p className="font-semibold text-primary">{getTypeClosing(dominantType)}</p>
            </div>
          </div>
        )}

        {/* CTA */}
        <div className="bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg shadow-xl p-8 mb-6 text-white text-center">
          <h3 className="text-2xl font-bold mb-3">🌟 この力をもっと伸ばしたい方へ</h3>
          <p className="mb-6">「相手の可能性を引き出す力」を学びませんか？</p>
          <a
            href="https://pro-coach.net/p/r/8uCeXl3l?free20=0030005"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-white text-purple-600 font-bold py-3 px-8 rounded-full hover:bg-gray-100 transition-all duration-200 hover:scale-105"
          >
            🎯 無料セミナーをチェック
          </a>
        </div>

        {/* メール送信 */}
        <div className="bg-white rounded-lg shadow-xl p-6 mb-6">
          <h3 className="text-xl font-bold text-gray-800 mb-2">📧 この結果を自分に送る</h3>
          <p className="text-gray-600 mb-3">後でゆっくり読み返せます</p>
          <div className="flex flex-col gap-3 items-center">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="example@mail.com"
              className="w-full max-w-md px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <button
              onClick={handleEmailSend}
              disabled={!email.includes('@')}
              className="w-full max-w-md bg-primary text-white font-medium py-2.5 px-6 rounded-lg hover:bg-blue-600 transition-all duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              📧 メールアプリを開く
            </button>
          </div>
        </div>

        {/* やり直しボタン */}
        <div className="text-center">
          <button
            onClick={onRestart}
            className="text-gray-600 hover:text-gray-800 font-medium py-2 px-6 rounded-lg hover:bg-white transition-all duration-200"
          >
            🔄 もう一度診断する
          </button>
        </div>
      </div>
    </div>
  );
}
