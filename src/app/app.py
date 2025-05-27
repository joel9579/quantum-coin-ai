from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/visual-dashboard')
def visual_dashboard():
    # Assuming coins like 'coin_bitcoin', etc.
    coin_visuals = {
        'coin_bitcoin': {
            'trend': url_for('static', filename='visuals/trend_bitcoin.png'),
            'summary': url_for('static', filename='visuals/summary_bitcoin.png')
        },
        # Add other coins here as needed
    }

    correlation_img = url_for('static', filename='visuals/correlation_matrix.png')

    return render_template('visual.html', coin_visuals=coin_visuals, correlation_img=correlation_img)

if __name__ == 'crypto_app':
    app.run(debug=True)
