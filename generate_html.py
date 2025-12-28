import csv
import json
import re

# CSVを読み込み
sales_data = []
encodings = ['utf-8', 'cp932', 'shift_jis', 'utf-8-sig']

for encoding in encodings:
    try:
        with open('plugin_data.csv', 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
            if 'プラグイン名' in content or 'セール価格' in content:
                break
    except:
        continue

def get_category(name):
    name_lower = name.lower()
    if 'comp' in name_lower:
        return {'icon': '🎚️', 'label': 'コンプ'}
    elif 'eq' in name_lower or 'equalizer' in name_lower:
        return {'icon': '🎛️', 'label': 'EQ'}
    elif 'reverb' in name_lower:
        return {'icon': '🌊', 'label': 'リバーブ'}
    elif 'delay' in name_lower:
        return {'icon': '⏱️', 'label': 'ディレイ'}
    elif 'synth' in name_lower:
        return {'icon': '🎹', 'label': 'シンセ'}
    elif 'drum' in name_lower or 'beat' in name_lower:
        return {'icon': '🥁', 'label': 'ドラム'}
    elif 'bass' in name_lower:
        return {'icon': '🎸', 'label': 'ベース'}
    elif 'vocal' in name_lower or 'voice' in name_lower:
        return {'icon': '🎤', 'label': 'ボーカル'}
    elif 'piano' in name_lower or 'key' in name_lower:
        return {'icon': '🎹', 'label': 'ピアノ/キー'}
    elif 'guitar' in name_lower:
        return {'icon': '🎸', 'label': 'ギター'}
    elif 'mastering' in name_lower:
        return {'icon': '💿', 'label': 'マスタリング'}
    elif 'limiter' in name_lower:
        return {'icon': '📊', 'label': 'リミッター'}
    elif 'saturator' in name_lower or 'distortion' in name_lower or 'overdrive' in name_lower:
        return {'icon': '🔥', 'label': 'サチュレーション'}
    elif 'chorus' in name_lower or 'flanger' in name_lower or 'phaser' in name_lower:
        return {'icon': '🌀', 'label': 'モジュレーション'}
    elif 'bundle' in name_lower:
        return {'icon': '📦', 'label': 'バンドル'}
    elif 'channel' in name_lower or 'strip' in name_lower:
        return {'icon': '🎚️', 'label': 'チャンネルストリップ'}
    elif 'metering' in name_lower or 'meter' in name_lower or 'analyzer' in name_lower:
        return {'icon': '📈', 'label': 'メーター'}
    else:
        return {'icon': '🎵', 'label': 'エフェクト'}

with open('plugin_data.csv', 'r', encoding=encoding, errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        keys = list(row.keys())
        
        name = row.get('プラグイン名', row.get(keys[0], '')) if keys else ''
        sale_price_str = row.get('セール価格', row.get(keys[1], '0')) if len(keys) > 1 else '0'
        original_price_str = row.get('定価', row.get(keys[2], '')) if len(keys) > 2 else ''
        discount = row.get('セール率', row.get(keys[3], '')) if len(keys) > 3 else ''
        end_date = row.get('終了日', row.get(keys[4], '')) if len(keys) > 4 else ''
        product_url = row.get('商品URL', row.get(keys[5], '')) if len(keys) > 5 else ''
        image_url = row.get('画像URL', row.get(keys[6], '')) if len(keys) > 6 else ''
        
        sale_price = int(''.join(filter(str.isdigit, str(sale_price_str)))) if sale_price_str else 0
        original_price = int(''.join(filter(str.isdigit, str(original_price_str)))) if original_price_str else 0
        savings = original_price - sale_price if original_price > sale_price else 0
        
        discount_match = re.search(r'(\d+)%', str(discount))
        discount_percent = int(discount_match.group(1)) if discount_match else 0
        
        category = get_category(name)
        
        sales_data.append({
            'name': name,
            'salePrice': sale_price,
            'originalPrice': original_price,
            'savings': savings,
            'discountPercent': discount_percent,
            'endDate': end_date,
            'productUrl': product_url,
            'imageUrl': image_url,
            'categoryIcon': category['icon'],
            'categoryLabel': category['label']
        })

sales_json = json.dumps(sales_data, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DTMプラグインセール情報 | 毎日更新</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Noto Sans JP', sans-serif;
            background: #0a0a0f;
            color: #fff;
            min-height: 100vh;
        }
        
        .header {
            text-align: center;
            padding: 40px 20px 24px;
            background: linear-gradient(180deg, #12121a 0%, #0a0a0f 100%);
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .header p {
            color: #666;
            font-size: 13px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 0 16px 40px;
        }
        
        /* おすすめ枠 */
        .picks-section {
            margin-bottom: 32px;
        }
        
        .section-title {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .picks-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 12px;
        }
        
        .pick-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid #2a2a4a;
            border-radius: 12px;
            padding: 16px;
            transition: all 0.2s;
        }
        
        .pick-card:hover {
            border-color: #5b5bf0;
            transform: translateY(-2px);
        }
        
        .pick-badge {
            display: inline-block;
            background: #f59e0b;
            color: #000;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
            margin-bottom: 8px;
        }
        
        .pick-name {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 6px;
            line-height: 1.4;
        }
        
        .pick-meta {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            font-size: 12px;
        }
        
        .pick-category {
            background: #2a2a3a;
            padding: 2px 8px;
            border-radius: 4px;
        }
        
        .pick-discount {
            color: #22c55e;
            font-weight: 700;
        }
        
        .pick-prices {
            display: flex;
            align-items: baseline;
            gap: 8px;
            margin-bottom: 12px;
        }
        
        .pick-price-sale {
            font-size: 20px;
            font-weight: 900;
            color: #22c55e;
        }
        
        .pick-price-original {
            font-size: 12px;
            color: #555;
            text-decoration: line-through;
        }
        
        .pick-cta {
            display: block;
            width: 100%;
            padding: 10px;
            background: linear-gradient(90deg, #f59e0b, #ef4444);
            color: #fff;
            text-align: center;
            text-decoration: none;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            transition: all 0.2s;
        }
        
        .pick-cta:hover {
            opacity: 0.9;
        }
        
        /* 安心情報 */
        .trust-bar {
            display: flex;
            justify-content: center;
            gap: 24px;
            padding: 16px;
            background: #111118;
            border-radius: 8px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }
        
        .trust-item {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: #888;
        }
        
        .filters {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 10px 20px;
            border: 1px solid #2a2a3a;
            border-radius: 25px;
            background: transparent;
            color: #888;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .filter-btn:hover {
            border-color: #5b5bf0;
            color: #5b5bf0;
        }
        
        .filter-btn.active {
            background: #5b5bf0;
            border-color: #5b5bf0;
            color: #fff;
        }
        
        .deals-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .deal-card {
            background: #14141c;
            border-radius: 10px;
            padding: 16px 20px;
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 16px;
            align-items: center;
            transition: all 0.2s;
            border: 1px solid transparent;
        }
        
        .deal-card:hover {
            background: #1a1a24;
            border-color: #2a2a3a;
        }
        
        .deal-card-urgent {
            border-left: 3px solid #ef4444;
            background: linear-gradient(90deg, rgba(239,68,68,0.1) 0%, #14141c 20%);
        }
        
        .deal-info {
            min-width: 0;
        }
        
        .deal-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 6px;
            flex-wrap: wrap;
        }
        
        .deal-category {
            font-size: 12px;
            color: #888;
            background: #1e1e2a;
            padding: 2px 8px;
            border-radius: 4px;
            white-space: nowrap;
        }
        
        .deal-name {
            font-size: 14px;
            font-weight: 600;
            color: #fff;
            line-height: 1.4;
        }
        
        .badge {
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 700;
            flex-shrink: 0;
        }
        
        .badge-discount {
            background: #dc2626;
            color: #fff;
        }
        
        .badge-urgent {
            background: #ef4444;
            color: #fff;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .deal-meta {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            font-size: 13px;
        }
        
        .deal-prices {
            display: flex;
            align-items: baseline;
            gap: 6px;
        }
        
        .price-sale {
            font-size: 20px;
            font-weight: 900;
            color: #22c55e;
        }
        
        .price-original {
            font-size: 12px;
            color: #555;
            text-decoration: line-through;
        }
        
        .deal-savings {
            color: #22c55e;
            font-size: 12px;
        }
        
        .deal-end {
            color: #666;
            font-size: 12px;
        }
        
        .deal-end-urgent {
            color: #ef4444;
            font-weight: 600;
            font-size: 12px;
        }
        
        .deal-action {
            flex-shrink: 0;
        }
        
        .cta-btn {
            display: inline-block;
            padding: 12px 20px;
            background: #5b5bf0;
            color: #fff;
            text-decoration: none;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.2s;
            white-space: nowrap;
        }
        
        .cta-btn:hover {
            background: #4a4ae0;
        }
        
        .cta-btn-urgent {
            background: linear-gradient(90deg, #ef4444, #f59e0b);
        }
        
        .cta-btn-urgent:hover {
            opacity: 0.9;
        }
        
        .footer {
            text-align: center;
            padding: 32px 20px;
            color: #444;
            font-size: 11px;
        }
        
        .footer a {
            color: #5b5bf0;
            text-decoration: none;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #555;
        }
        
        /* スマホ対応 */
        @media (max-width: 640px) {
            .header { padding: 32px 16px 20px; }
            .header h1 { font-size: 20px; }
            
            .trust-bar {
                gap: 16px;
                padding: 12px;
            }
            
            .trust-item { font-size: 11px; }
            
            .picks-grid {
                grid-template-columns: 1fr;
            }
            
            .deal-card {
                grid-template-columns: 1fr;
                gap: 12px;
                padding: 14px;
            }
            
            .deal-name { font-size: 13px; }
            .price-sale { font-size: 18px; }
            
            .cta-btn {
                width: 100%;
                text-align: center;
                padding: 14px;
            }
            
            .filter-btn {
                padding: 8px 14px;
                font-size: 12px;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <h1>🎹 DTMプラグインセール情報</h1>
        <p>Plugin Boutique のセール情報を毎日自動更新</p>
    </header>
    
    <div class="container">
        <!-- 安心情報バー -->
        <div class="trust-bar">
            <div class="trust-item">✅ 公式ストア直リンク</div>
            <div class="trust-item">🔒 安全な決済</div>
            <div class="trust-item">📧 購入後すぐにライセンス届く</div>
        </div>
        
        <!-- おすすめピック -->
        <div class="picks-section" id="picks-section"></div>
        
        <!-- フィルター -->
        <div class="filters">
            <button class="filter-btn active" data-filter="all">すべて</button>
            <button class="filter-btn" data-filter="50">50%OFF以上</button>
            <button class="filter-btn" data-filter="70">70%OFF以上</button>
            <button class="filter-btn" data-filter="90">90%OFF以上</button>
        </div>
        
        <!-- セール一覧 -->
        <div class="deals-list" id="deals"></div>
    </div>
    
    <footer class="footer">
        <p>データ: <a href="https://www.pluginboutique.com/" target="_blank">Plugin Boutique</a> | 価格は変動する場合があります</p>
    </footer>
    
    <script>
        const salesData = ''' + sales_json + ''';
        
        function parseEndDate(dateStr) {
            if (!dateStr) return new Date('2099-12-31');
            const match = dateStr.match(/Ends\\s+(\\d+)\\s+(\\w+)/);
            if (!match) return new Date('2099-12-31');
            const day = parseInt(match[1]);
            const monthStr = match[2];
            const months = {Jan:0,Feb:1,Mar:2,Apr:3,May:4,Jun:5,Jul:6,Aug:7,Sep:8,Oct:9,Nov:10,Dec:11};
            const month = months[monthStr] !== undefined ? months[monthStr] : 0;
            
            const now = new Date();
            let year = now.getFullYear();
            if (now.getMonth() >= 10 && month <= 2) year++;
            
            return new Date(year, month, day);
        }
        
        function getDaysRemaining(dateStr) {
            const end = parseEndDate(dateStr);
            const now = new Date();
            now.setHours(0,0,0,0);
            return Math.ceil((end - now) / (1000 * 60 * 60 * 24));
        }
        
        salesData.sort((a, b) => parseEndDate(a.endDate) - parseEndDate(b.endDate));
        
        // おすすめピック: 70%以上OFF + 残り7日以内から最大3件
        function renderPicks() {
            const picks = salesData
                .filter(d => d.discountPercent >= 70 && getDaysRemaining(d.endDate) <= 7)
                .slice(0, 3);
            
            if (picks.length === 0) return;
            
            const section = document.getElementById('picks-section');
            section.innerHTML = `
                <div class="section-title">🔥 今週のおすすめ</div>
                <div class="picks-grid">
                    ${picks.map(deal => {
                        const days = getDaysRemaining(deal.endDate);
                        return `
                            <div class="pick-card">
                                <span class="pick-badge">残り${days}日 / ${deal.discountPercent}%OFF</span>
                                <div class="pick-name">${deal.name}</div>
                                <div class="pick-meta">
                                    <span class="pick-category">${deal.categoryIcon} ${deal.categoryLabel}</span>
                                </div>
                                <div class="pick-prices">
                                    <span class="pick-price-sale">¥${deal.salePrice.toLocaleString()}</span>
                                    <span class="pick-price-original">¥${deal.originalPrice.toLocaleString()}</span>
                                </div>
                                <a href="${deal.productUrl}" target="_blank" class="pick-cta">🔥 今すぐチェック</a>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        }
        
        let currentFilter = 'all';
        
        function renderDeals() {
            const container = document.getElementById('deals');
            container.innerHTML = '';
            
            const filtered = currentFilter === 'all' 
                ? salesData 
                : salesData.filter(d => d.discountPercent >= parseInt(currentFilter));
            
            if (filtered.length === 0) {
                container.innerHTML = '<div class="empty-state">該当するセールはありません</div>';
                return;
            }
            
            filtered.forEach(deal => {
                const days = getDaysRemaining(deal.endDate);
                const isUrgent = days <= 3;
                
                const card = document.createElement('div');
                card.className = 'deal-card' + (isUrgent ? ' deal-card-urgent' : '');
                
                const endText = days <= 7 ? `残り${days}日` : deal.endDate.replace('Ends ', '');
                const endClass = isUrgent ? 'deal-end-urgent' : 'deal-end';
                
                card.innerHTML = `
                    <div class="deal-info">
                        <div class="deal-header">
                            <span class="deal-category">${deal.categoryIcon} ${deal.categoryLabel}</span>
                            <span class="deal-name">${deal.name}</span>
                        </div>
                        <div class="deal-meta">
                            <div class="deal-prices">
                                <span class="price-sale">¥${deal.salePrice.toLocaleString()}</span>
                                <span class="price-original">¥${deal.originalPrice.toLocaleString()}</span>
                            </div>
                            <span class="badge badge-discount">${deal.discountPercent}%OFF</span>
                            ${isUrgent ? '<span class="badge badge-urgent">⚠ まもなく終了</span>' : ''}
                            <span class="deal-savings">¥${deal.savings.toLocaleString()} お得</span>
                            <span class="${endClass}">${endText}</span>
                        </div>
                    </div>
                    <div class="deal-action">
                        <a href="${deal.productUrl}" target="_blank" class="cta-btn${isUrgent ? ' cta-btn-urgent' : ''}">セール価格で購入</a>
                    </div>
                `;
                container.appendChild(card);
            });
        }
        
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                renderDeals();
            });
        });
        
        renderPicks();
        renderDeals();
    </script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated index.html with {len(sales_data)} items")
