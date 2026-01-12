export interface VAKQuestion {
  id: number;
  type: 'V' | 'A' | 'K';
  question: string;
}

export interface VAKScores {
  V: number;
  A: number;
  K: number;
}

export interface VAKTypeInfo {
  title: string;
  description: string;
  strengths: string[];
  businessTips: string[];
  wineTips: string[];
  relationshipTips: string[];
}

// 12問の質問（シャッフル済み）
export const VAK_QUESTIONS: VAKQuestion[] = [
  { id: 1, type: 'A', question: '会話を通じて相手のことを理解し、信頼関係を築くのが得意だ' },
  { id: 2, type: 'V', question: '新しい情報や提案を受けるとき、資料やデータで見せてもらうと理解しやすい' },
  { id: 3, type: 'K', question: '実際に体験することで、最も深く理解し記憶に残る' },
  { id: 4, type: 'V', question: '人と会ったとき、相手の表情や雰囲気から多くの情報を読み取る' },
  { id: 5, type: 'A', question: '人の話を聞いて、その背景や想いを汲み取ることができる' },
  { id: 6, type: 'K', question: '直感や雰囲気を大切にして、判断することが多い' },
  { id: 7, type: 'V', question: '場所や人の顔を視覚的に覚えるのが得意で、次に会ったときすぐに分かる' },
  { id: 8, type: 'A', question: '声のトーンや話し方から、相手の本音や感情を読み取れる' },
  { id: 9, type: 'K', question: '理論より実践、まず試してみることで学ぶのが好きだ' },
  { id: 10, type: 'V', question: 'プレゼンや説明を受けるとき、図やグラフがあると理解が早い' },
  { id: 11, type: 'A', question: 'ストーリーや事例を聞くことで、物事への興味や理解が深まる' },
  { id: 12, type: 'K', question: '人と話すとき、その場の空気感や雰囲気から相手の気持ちを感じ取る' },
];

// タイプ情報
export const TYPE_INFO: Record<'V' | 'A' | 'K', VAKTypeInfo> = {
  V: {
    title: '👀 見るタイプ（視覚型）',
    description: '目から入る情報が得意で、見て理解するタイプです。',
    strengths: [
      'データや資料、図解で理解しやすい',
      '相手の表情やボディランゲージを読み取る',
      '視覚的な記憶が得意',
      '見た目や雰囲気を大切にする'
    ],
    businessTips: [
      'プレゼンには視覚資料を効果的に使う',
      '商談では実物やサンプルを見せる',
      'ホワイトボードや図解で説明する',
      '身だしなみや会議室の雰囲気づくりを意識'
    ],
    wineTips: [
      'ワインの色や輝きの違いを楽しむ',
      'ラベルや産地の写真に注目',
      'テーブルセッティングを楽しむ'
    ],
    relationshipTips: [
      '資料やビジュアルを用意して説明',
      '身振りや表情豊かに話す',
      '清潔感のある身だしなみを心がける'
    ]
  },
  A: {
    title: '👂 聞くタイプ（聴覚型）',
    description: '耳から入る情報が得意で、会話や説明を通じて理解するタイプです。',
    strengths: [
      '話を聞いて理解するのが得意',
      '会話で信頼関係を築く',
      '声のトーンから感情を読み取る',
      'ストーリーや背景に興味を持つ'
    ],
    businessTips: [
      '丁寧な説明と対話を大切に',
      '電話やオンライン会議を効果的に活用',
      'グループディスカッションに積極参加',
      '相手の話をよく聞き、質問する'
    ],
    wineTips: [
      'ソムリエの説明に耳を傾ける',
      'ワインの背景やストーリーを楽しむ',
      '参加者との会話を楽しむ'
    ],
    relationshipTips: [
      'じっくり話を聞く時間を作る',
      '背景や理由を丁寧に説明',
      'ストーリーを交えて伝える'
    ]
  },
  K: {
    title: '✋ 体感タイプ（体感覚型）',
    description: '体で感じて理解するのが得意で、体験や実践を通じて学ぶタイプです。',
    strengths: [
      '実際に体験することで深く理解',
      '直感や雰囲気を大切にする',
      '実践的なアプローチが好き',
      '身体で感じる感覚に敏感'
    ],
    businessTips: [
      '実践的なワークショップに参加',
      'まず試してみる、体験する',
      'ロールプレイで理解を深める',
      '現場や実物を見て判断'
    ],
    wineTips: [
      '実際に味わいながら学ぶ',
      '香りをじっくり楽しむ',
      '料理とのペアリングを試す'
    ],
    relationshipTips: [
      '実際に体験できる機会を提供',
      'デモやサンプルを用意',
      '理論より実践を重視',
      'リラックスできる雰囲気づくり'
    ]
  }
};

// スコア計算
export function calculateScores(answers: Record<number, number>): VAKScores {
  const scores: VAKScores = { V: 0, A: 0, K: 0 };
  
  VAK_QUESTIONS.forEach(q => {
    const answer = answers[q.id];
    if (answer) {
      scores[q.type] += answer;
    }
  });
  
  return scores;
}

// 優勢タイプ判定
export function getDominantType(scores: VAKScores): 'V' | 'A' | 'K' | 'balanced' {
  const maxScore = Math.max(scores.V, scores.A, scores.K);
  const minScore = Math.min(scores.V, scores.A, scores.K);
  
  // バランス型判定（差が3未満）
  if (maxScore - minScore < 3) {
    return 'balanced';
  }
  
  // 優勢型判定
  if (scores.V === maxScore) return 'V';
  if (scores.A === maxScore) return 'A';
  return 'K';
}

// タイプ名取得
export function getTypeName(type: 'V' | 'A' | 'K' | 'balanced'): string {
  if (type === 'balanced') return 'バランス型';
  const names = {
    V: '見るタイプ（視覚型）',
    A: '聞くタイプ（聴覚型）',
    K: '体感タイプ（体感覚型）'
  };
  return names[type];
}

// タイプ別締めくくり文言
export function getTypeClosing(type: 'V' | 'A' | 'K' | 'balanced'): string {
  const closings = {
    V: '視覚で人を動かすこの才能は、プレゼンテーションや営業で力を発揮します。',
    A: '傾聴で信頼を築くこの才能は、カウンセリングやコーチングで力を発揮します。',
    K: '体感で場を読むこの才能は、現場マネジメントやチーム作りで力を発揮します。',
    balanced: 'あらゆる状況に対応できるこの才能は、チームリーダーやコーチに最適です。'
  };
  return closings[type];
}
