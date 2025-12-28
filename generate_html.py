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
        
        sales_data.append({
            'name': name,
            'salePrice': sale_price,
            'originalPrice': original_price,
            'savings': savings,
            'discountPercent': discount_percent,
            'endDate': end_date,
            'productUrl': product_url,
            'imageUrl': image_url
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
            padding: 40px 20px 32px;
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
            gap: 12px;
        }
        
        .deal-card {
            background: #14141c;
            border-radius: 12px;
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 16px;
            align-items: center;
            transition: all 0.2s;
            border: 1px solid #1e1e2a;
        }
        
        .deal-card:hover {
            background: #1a1a24;
            border-color: #2a2a3a;
        }
        
        .deal-card-urgent {
            border-left: 3px solid #ef4444;
        }
        
        .deal-info {
            min-width: 0;
        }
        
        .deal-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            flex-wrap: wrap;
        }
        
        .deal-name {
            font-size: 15px;
            font-weight: 600;
            color: #fff;
            line-height: 1.4;
        }
        
        .badge {
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            flex-shrink: 0;
        }
        
        .badge-discount {
            background: #dc2626;
            color: #fff;
        }
        
        .badge-urgent {
            background: #f59e0b;
            color: #000;
        }
        
        .deal-meta {
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            font-size: 13px;
        }
        
        .deal-prices {
            display: flex;
            align-items: baseline;
            gap: 8px;
        }
        
        .price-sale {
            font-size: 22px;
            font-weight: 900;
            color: #22c55e;
        }
        
        .price-original {
            font-size: 13px;
            color: #555;
            text-decoration: line-through;
        }
        
        .deal-savings {
            color: #22c55e;
            font-weight: 500;
        }
        
        .deal-end {
            color: #666;
        }
        
        .deal-end-urgent {
            color: #ef4444;
            font-weight: 600;
        }
        
        .deal-action {
            flex-shrink: 0;
        }
        
        .cta-btn {
            display: inline-block;
            padding: 12px 24px;
            background: #5b5bf0;
            color: #fff;
            text-decoration: none;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s;
            white-space: nowrap;
        }
        
        .cta-btn:hover {
            background: #4a4ae0;
            transform: translateY(-1px);
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
            .header { padding: 32px 16px 24px; }
            .header h1 { font-size: 20px; }
            
            .deal-card {
                grid-template-columns: 1fr;
                gap: 12px;
                padding: 16px;
            }
            
            .deal-name {
                font-size: 14px;
            }
            
            .price-sale {
                font-size: 20px;
            }
            
            .deal-meta {
                gap: 12px;
            }
            
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
        <div class="filters">
            <button class="filter-btn active" data-filter="all">すべて</button>
            <button class="filter-btn" data-filter="50">50%OFF以上</button>
            <button class="filter-btn" data-filter="70">70%OFF以上</button>
            <button class="filter-btn" data-filter="90">90%OFF以上</button>
        </div>
        
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
                            <span class="deal-name">${deal.name}</span>
                            <span class="badge badge-discount">${deal.discountPercent}%OFF</span>
                            ${isUrgent ? '<span class="badge badge-urgent">まもなく終了</span>' : ''}
                        </div>
                        <div class="deal-meta">
                            <div class="deal-prices">
                                <span class="price-sale">¥${deal.salePrice.toLocaleString()}</span>
                                <span class="price-original">¥${deal.originalPrice.toLocaleString()}</span>
                            </div>
                            <span class="deal-savings">¥${deal.savings.toLocaleString()} お得</span>
                            <span class="${endClass}">${endText}</span>
                        </div>
                    </div>
                    <div class="deal-action">
                        <a href="${deal.productUrl}" target="_blank" class="cta-btn">詳細を見る</a>
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
        
        renderDeals();
    </script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated index.html with {len(sales_data)} items")
