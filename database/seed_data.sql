INSERT INTO sources (name, url, feed_url) VALUES
('moneycontrol', 'https://www.moneycontrol.com', 'https://www.moneycontrol.com/rss/MCtopnews.xml'),
('economic_times', 'https://economictimes.indiatimes.com', 'https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms'),
('livemint', 'https://www.livemint.com', 'https://www.livemint.com/rss/markets')
ON CONFLICT (name) DO NOTHING;

INSERT INTO companies (name, ticker, sector, aliases) VALUES
('Infosys', 'INFY', 'IT', ARRAY['Infosys Limited', 'INFY']),
('Tata Consultancy Services', 'TCS', 'IT', ARRAY['TCS', 'Tata Consulting']),
('Wipro', 'WIPRO', 'IT', ARRAY['Wipro Limited']),
('HCL Technologies', 'HCLTECH', 'IT', ARRAY['HCL Tech', 'HCL']),
('Tech Mahindra', 'TECHM', 'IT', ARRAY['Tech M']),
('HDFC Bank', 'HDFCBANK', 'Banking', ARRAY['HDFC', 'HDFCBANK']),
('ICICI Bank', 'ICICIBANK', 'Banking', ARRAY['ICICI']),
('State Bank of India', 'SBIN', 'Banking', ARRAY['SBI', 'State Bank']),
('Axis Bank', 'AXISBANK', 'Banking', ARRAY['Axis']),
('Kotak Mahindra Bank', 'KOTAKBANK', 'Banking', ARRAY['Kotak']),
('Reliance Industries', 'RELIANCE', 'Energy', ARRAY['Reliance', 'RIL']),
('ONGC', 'ONGC', 'Energy', ARRAY['Oil and Natural Gas', 'ONGC Limited']),
('Indian Oil', 'IOC', 'Energy', ARRAY['IOC', 'Indian Oil Corporation']),
('Hindustan Unilever', 'HINDUNILVR', 'FMCG', ARRAY['HUL', 'Hindustan Unilever Limited']),
('ITC', 'ITC', 'FMCG', ARRAY['ITC Limited']),
('Nestle India', 'NESTLEIND', 'FMCG', ARRAY['Nestle']),
('Sun Pharmaceutical', 'SUNPHARMA', 'Pharma', ARRAY['Sun Pharma']),
('Dr Reddys', 'DRREDDY', 'Pharma', ARRAY['Dr Reddy', 'DRL']),
('Cipla', 'CIPLA', 'Pharma', ARRAY['Cipla Limited']),
('Maruti Suzuki', 'MARUTI', 'Auto', ARRAY['Maruti']),
('Tata Motors', 'TATAMOTORS', 'Auto', ARRAY['Tata Motor']),
('Mahindra', 'M&M', 'Auto', ARRAY['M&M', 'Mahindra and Mahindra'])
ON CONFLICT (name) DO NOTHING;