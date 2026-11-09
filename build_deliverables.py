import os
import zipfile
import subprocess
import base64

base_dir = r"C:\Users\Nisarg\.gemini\antigravity\scratch\ieee_fdi_ev_paper"
img_dir = os.path.join(base_dir, "images")
zip_path = os.path.join(base_dir, "Overleaf_Project_Team20.zip")
html_path = os.path.join(base_dir, "paper_ieee.html")
pdf_path = os.path.join(base_dir, "IEEE_FDI_EV_Charging_NARX.pdf")

# 1. Create Overleaf ZIP Package
print("Creating Overleaf ZIP archive...")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Add main.tex
    zipf.write(os.path.join(base_dir, "main.tex"), arcname="main.tex")
    # Add references.bib
    zipf.write(os.path.join(base_dir, "references.bib"), arcname="references.bib")
    # Add images
    for fname in ["fig1_flowchart.png", "fig2_attack_iqr.png", "fig3_comparison.png", "fig4_opal_rt.png"]:
        fpath = os.path.join(img_dir, fname)
        if os.path.exists(fpath):
            zipf.write(fpath, arcname=f"images/{fname}")
            print(f"Added images/{fname}")

print(f"Overleaf ZIP created at: {zip_path} ({os.path.getsize(zip_path)} bytes)")

# 2. Encode images to base64 for standalone HTML rendering
def get_b64(fname):
    with open(os.path.join(img_dir, fname), "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

img1_b64 = get_b64("fig1_flowchart.png")
img2_b64 = get_b64("fig2_attack_iqr.png")
img3_b64 = get_b64("fig3_comparison.png")
img4_b64 = get_b64("fig4_opal_rt.png")

# 3. Create IEEE HTML Document
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>False Data Injection Attack Detection in EV Charging Network Using NARX Neural Network</title>
<style>
  @page {{
    size: letter;
    margin-top: 19mm;
    margin-bottom: 19mm;
    margin-left: 15mm;
    margin-right: 15mm;
    @bottom-center {{
      content: counter(page);
      font-family: 'Times New Roman', serif;
      font-size: 9pt;
    }}
  }}

  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 10pt;
    line-height: 1.18;
    color: #000;
    margin: 0;
    padding: 0;
    background-color: #fff;
  }}

  /* Title & Author Block (Single Column Spanning) */
  .title-block {{
    text-align: center;
    margin-bottom: 18px;
  }}

  .paper-title {{
    font-size: 22pt;
    font-weight: bold;
    line-height: 1.2;
    margin-bottom: 6px;
  }}

  .sub-title {{
    font-size: 13pt;
    font-weight: bold;
    color: #222;
    margin-bottom: 14px;
  }}

  .author-container {{
    display: flex;
    justify-content: center;
    text-align: center;
    margin-bottom: 6px;
    font-size: 10pt;
  }}

  .author-box {{
    margin: 0 18px;
  }}

  .author-names {{
    font-size: 10.5pt;
    font-weight: bold;
    margin-bottom: 3px;
  }}

  .affiliation {{
    font-size: 9.5pt;
    font-style: italic;
    line-height: 1.25;
  }}

  .advisor {{
    font-size: 9.5pt;
    font-weight: bold;
    color: #111;
    margin-top: 4px;
  }}

  /* Two Column Layout */
  .content-columns {{
    column-count: 2;
    column-gap: 18px;
    column-fill: balance;
    text-align: justify;
    text-justify: inter-word;
  }}

  /* Abstract & Index Terms */
  .abstract-box {{
    font-size: 9pt;
    line-height: 1.2;
    margin-bottom: 12px;
  }}

  .abstract-heading {{
    font-weight: bold;
    font-style: italic;
  }}

  .index-terms {{
    font-size: 9pt;
    margin-top: 6px;
    margin-bottom: 14px;
  }}

  .index-heading {{
    font-weight: bold;
    font-style: italic;
  }}

  /* Headings */
  h1.sec-heading {{
    font-size: 10pt;
    font-weight: bold;
    text-transform: uppercase;
    text-align: center;
    margin-top: 14px;
    margin-bottom: 6px;
    letter-spacing: 0.8px;
    break-after: avoid;
  }}

  h2.subsec-heading {{
    font-size: 10pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 10px;
    margin-bottom: 4px;
    break-after: avoid;
  }}

  p {{
    text-indent: 14px;
    margin: 0 0 5px 0;
  }}

  p.no-indent {{
    text-indent: 0;
  }}

  /* Equations */
  .equation {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 7px 0;
    padding: 0 8px;
    font-style: italic;
    font-size: 9.5pt;
  }}

  .eq-math {{
    margin: 0 auto;
    font-family: 'Cambria Math', 'Times New Roman', serif;
  }}

  .eq-num {{
    font-style: normal;
    font-size: 9.5pt;
  }}

  /* Figures & Tables */
  figure {{
    margin: 10px 0;
    text-align: center;
    break-inside: avoid;
  }}

  figure.span-cols {{
    column-span: all;
    margin: 14px auto;
  }}

  figure img {{
    width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
    border: 1px solid #ddd;
  }}

  figcaption {{
    font-size: 8.5pt;
    text-align: justify;
    margin-top: 5px;
    line-height: 1.2;
  }}

  figcaption strong {{
    font-weight: bold;
  }}

  table.ieee-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 8pt;
    line-height: 1.2;
    break-inside: avoid;
  }}

  table.ieee-table th, table.ieee-table td {{
    padding: 4px 6px;
    text-align: center;
    white-space: nowrap;
  }}

  table.ieee-table th {{
    font-weight: bold;
    border-top: 1.5px solid #000;
    border-bottom: 1px solid #000;
    background-color: #fcfcfc;
  }}

  table.ieee-table td {{
    border-bottom: 0.5px solid #ddd;
  }}

  table.ieee-table tr.last-row td {{
    border-bottom: 1.5px solid #000;
  }}

  .table-title {{
    font-size: 8.5pt;
    text-align: center;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 8px;
    margin-bottom: 3px;
  }}

  /* Bullet lists */
  ul, ol {{
    margin: 4px 0 6px 16px;
    padding: 0;
    font-size: 9.5pt;
  }}

  li {{
    margin-bottom: 3px;
    line-height: 1.2;
  }}

  /* References */
  .references-list {{
    font-size: 8pt;
    line-height: 1.2;
    margin-top: 6px;
  }}

  .ref-item {{
    text-indent: -18px;
    margin-left: 18px;
    margin-bottom: 4px;
  }}
</style>
</head>
<body>

<div class="title-block">
  <div class="paper-title">False Data Injection Attack Detection in EV Charging Network Using NARX Neural Network</div>
  
  <div class="author-container">
    <div class="author-box">
      <div class="author-names">Sumit Kumar (CS23B2008), Nisarg Rande (CS23B1090), and Jatin Goyal (CS23B2045)</div>
      <div class="affiliation">Department of Computer Science and Engineering<br>Indian Institute of Information Technology Design and Manufacturing</div>
      <div class="advisor">Faculty Advisor: Dr. Pradeep Kumar Bhale</div>
    </div>
  </div>
</div>

<div class="content-columns">

  <div class="abstract-box">
    <span class="abstract-heading">Abstract</span>—Electric vehicle (EV) charging stations rely heavily on Internet-of-Things (IoT) communication networks to schedule sessions, exchange power demand parameters, and manage grid stability. However, open communication channels between users, EV supply equipment (EVSE), and central management systems (CMS) introduce serious vulnerabilities to false data injection (FDI) attacks. Existing detection schemes rely either on physics-based grid models that require exact system parameters or on machine learning classifiers that fail completely when trained on highly imbalanced real-world datasets. In this report, we present a model-free, regression-based attack detection framework utilizing a Nonlinear Autoregressive Exogenous (NARX) neural network. The NARX model forecasts the continuous energy delivery profile based on user charging preferences. The resulting Error of Estimation (EoE) is statistically evaluated using the Interquartile Range (IQR) method combined with a temporal consecutive spike windowing mechanism (<i>q</i> = 5). We evaluate the proposed framework on the real-world Caltech Adaptive Charging Network (ACN) dataset comprising 47,095 samples. The proposed NARX framework achieves an attack detection accuracy of 99.40% and an F1-score of 84.40%, drastically outperforming conventional Feedforward Neural Networks (88.68% accuracy, 19.60% F1-score) and LSTM classification baselines (98.00% accuracy, 0.00% F1-score). Furthermore, real-time hardware-in-the-loop validation on an OPAL-RT simulator confirms that stealthy FDI attacks are reliably flagged within 5 seconds. Finally, we propose concrete technical extensions for subsequent project reviews, including adaptive thresholding and attention-based temporal modeling.
  </div>

  <div class="index-terms">
    <span class="index-heading">Index Terms</span>—Cyber-physical security, electric vehicles (EVs), false data injection (FDI), NARX neural network, interquartile range (IQR), OPAL-RT, smart microgrids.
  </div>

  <h1 class="sec-heading">I. Introduction</h1>
  <p>The rapid expansion of electric vehicles (EVs) and plug-in hybrid electric vehicles (PHEVs) has established public EV charging stations (EVCSs) as critical components of smart distribution microgrids [1]. Modern EV supply equipment (EVSE) integrates Internet-of-Things (IoT) controllers that support automated slot reservation, dynamic tariff pricing, real-time demand-response negotiation, and payment verification via mobile applications [2].</p>

  <p>Although these connected technologies enhance user convenience and station utilization, they expand the cyber-attack surface across power distribution networks [3]. Communication links connecting EV drivers, field chargers, and cloud-hosted Central Management Systems (CMSs) frequently lack authenticated end-to-end cryptographic verification. This permits adversaries to execute stealthy False Data Injection (FDI) attacks [4]. Rather than triggering catastrophic hardware failures or abrupt power dropouts, a stealthy FDI attack targets individual vehicle sessions by subtly altering user-supplied charging preferences [8]. By mimicking benign user variations, such attacks bypass standard threshold alarms, resulting in premature charging suspension, battery health degradation, localized load instability, and operator revenue disruption.</p>

  <p>Detecting stealthy FDI attacks presents fundamental technical challenges that existing methodologies fail to address effectively:</p>
  <ul>
    <li><b>Model-Based (Physics-Based) Methods:</b> These approaches rely on precise mathematical models of the microgrid, including transformer admittances, power converter state equations, and battery electrochemical properties [5]. In commercial stations, battery temperature variations, unpredictable vehicle connection times, and measurement noise introduce severe model mismatches, triggering frequent false alarms.</li>
    <li><b>Machine Learning (ML) Classifiers:</b> Supervised classifiers (e.g., LSTMs, CNNs, Decision Trees) treat attack detection as a discrete classification problem (attack vs. non-attack) [9, 10]. In operational charging logs, malicious incidents represent rare anomalies in vast seas of nominal data. This severe class imbalance causes classifier algorithms to heavily favor the majority non-attack class, yielding 0% recall and 0% F1-score on actual intrusions.</li>
  </ul>

  <p>To overcome both challenges, this work implements a model-free, regression-based detection framework using a Nonlinear Autoregressive Exogenous (NARX) neural network [1]. By learning to estimate continuous energy delivery over time, the NARX network quantifies deviations as the Error of Estimation (EoE), which is subsequently filtered using Interquartile Range (IQR) statistics and a consecutive spike windowing mechanism (<i>q</i> = 5).</p>

  <figure class="span-cols">
    <img src="data:image/png;base64,{img1_b64}" alt="End-to-End System Pipeline">
    <figcaption><strong>Fig. 1.</strong> End-to-end system flowchart: EV user parameter exchange, communication protocols (HTTP/OCPP), stealthy FDI attack injection via ID spoofing/MitM, closed-loop NARX energy estimation, EoE computation, IQR statistical bounding, and consecutive spike window alerting.</figcaption>
  </figure>

  <h1 class="sec-heading">II. System Architecture & Threat Model</h1>

  <h2 class="subsec-heading">A. Protocol Stack and Cyber Vulnerabilities</h2>
  <p>An IoT-enabled EVCS infrastructure relies on three primary communication tiers, as depicted in Fig. 1:</p>
  <ol>
    <li><b>User-to-CMS (HTTP/HTTPS):</b> Drivers utilize mobile applications to schedule reservations, submit energy requirements, and register departure schedules. Weak session authentication tokens and web API endpoints remain vulnerable to phishing, token hijacking, and identity (ID) spoofing attacks [6].</li>
    <li><b>EVSE-to-CMS (OCPP):</b> The Open Charge Point Protocol coordinates charging rate caps, heartbeat telemetry, and billing status between physical chargers and the central server [11]. Unencrypted OCPP channels allow Man-in-the-Middle (MitM) message modification.</li>
    <li><b>EVSE-to-BMS (IEC 61851 / ISO 15118):</b> Charging rate negotiation and battery State-of-Charge (SoC) updates are managed via control pilot signals and PLC transceivers. Analog pilot signal manipulation can abruptly interrupt power transfer [2].</li>
  </ol>

  <h2 class="subsec-heading">B. Stealthy FDI Attack Formulation</h2>
  <p>When user <i>U<sub>l</sub></i> plugs vehicle <i>n</i> into EVSE <i>m</i> at time <i>t</i>, the user enters four parameters: Start Time (<i>ST<sub>t</sub><sup>n</sup></i>), End Time (<i>ET<sub>t</sub><sup>n</sup></i>), Energy Demanded (<i>ED<sub>t</sub><sup>n</sup></i>), and Minutes Available (<i>MA<sub>t</sub><sup>n</sup></i>). The CMS calculates an optimal charging session profile <i>CS<sub>t</sub><sup>n</sup></i>:</p>

  <div class="equation">
    <span class="eq-math">CS<sub>t</sub><sup>n</sup> = f(ST<sub>t</sub><sup>n</sup>, ET<sub>t</sub><sup>n</sup>, ED<sub>t</sub><sup>n</sup>, MA<sub>t</sub><sup>n</sup>)</span>
    <span class="eq-num">(1)</span>
  </div>

  <p>Under normal conditions, users may alter their available minutes at time <i>t + &Delta;t</i> to update the charging duration. The attacker exploits this valid update feature by intercepting the HTTP request and injecting an unauthorized deviation &plusmn;&phi;:</p>

  <div class="equation">
    <span class="eq-math">MA<sub>t+&Delta;t</sub><sup>n, adv</sup> = MA<sub>t</sub><sup>n</sup> &plusmn; &phi;</span>
    <span class="eq-num">(2)</span>
  </div>

  <div class="equation">
    <span class="eq-math">CS<sub>t+&Delta;t</sub><sup>n, adv</sup> = f(ST<sub>t</sub><sup>n</sup>, ET<sub>t</sub><sup>n</sup>, ED<sub>t</sub><sup>n</sup>, MA<sub>t+&Delta;t</sub><sup>n, adv</sup>)</span>
    <span class="eq-num">(3)</span>
  </div>

  <p>Because charging algorithms prioritize vehicles with shorter dwell times (<i>MA</i>) to maximize bay throughput, falsely reducing <i>MA</i> disrupts the scheduled current <i>I(t)</i> and power <i>P(t) = V(t) &middot; I(t)</i>. If the forged duration falls below the current session runtime, the EVSE halts charging completely. Because the manipulated parameters remain within syntactically valid ranges, perimeter security filters fail to flag the intrusion.</p>

  <figure class="span-cols">
    <img src="data:image/png;base64,{img2_b64}" alt="Energy Estimation and IQR Plot">
    <figcaption><strong>Fig. 2.</strong> (a) Actual delivered energy <i>y(t)</i> vs. closed-loop NARX estimated energy <i>&ycirc;(t)</i> under a stealthy FDI attack halting charging. (b) EoE time-series with data-driven IQR upper and lower bounds, highlighting consecutive spike detection (<i>q</i> = 5) triggering the FDI attack alert.</figcaption>
  </figure>

  <h1 class="sec-heading">III. Proposed NARX-IQR Detection Framework</h1>

  <h2 class="subsec-heading">A. NARX Neural Network Architecture</h2>
  <p>The NARX network is a dynamic recurrent neural network equipped with multi-step delay feedback [12]. It relates the continuous delivered energy <i>y(t)</i> (in kWh per timestamp) to past values of exogenous user inputs <i>x(t)</i> and past values of endogenous model outputs <i>y(t)</i>:</p>

  <div class="equation">
    <span class="eq-math">y(t) = F(x(t-1), &hellip;, x(t-m<sub>x</sub>), y(t-1), &hellip;, y(t-m<sub>y</sub>))</span>
    <span class="eq-num">(4)</span>
  </div>

  <p>where <i>m<sub>x</sub></i> and <i>m<sub>y</sub></i> represent input and output memory orders. To ensure real-time execution on edge controllers while preventing overfitting, the network is configured with:</p>
  <ul>
    <li><b>Input Layer:</b> 4 exogenous features (<i>ST, ET, ED, MA</i>) and feedback lags with memory orders <i>m<sub>x</sub> = m<sub>y</sub> = 2</i>.</li>
    <li><b>Hidden Layer:</b> A single hidden layer of 10 neurons with sigmoid activation functions, optimized using Levenberg-Marquardt backpropagation.</li>
    <li><b>Output Layer:</b> A linear unit forecasting continuous energy delivered <i>&ycirc;(t)</i>:</li>
  </ul>

  <div class="equation">
    <span class="eq-math">&ycirc;(t) = F<sub>out</sub>(w<sub>out</sub> &middot; F<sub>hid</sub>(w<sub>hid</sub> U(t-1) + b<sub>hid</sub>) + b<sub>out</sub>)</span>
    <span class="eq-num">(5)</span>
  </div>

  <p>The network is trained in series-parallel (open-loop) mode and executed online in parallel (closed-loop) mode where predicted energy values are fed back recursively.</p>

  <h2 class="subsec-heading">B. Error of Estimation (EoE) Metric</h2>
  <p>At each timestamp <i>t</i>, the residual deviation between the physical EVSE meter measurement <i>y(t)</i> and the NARX projection <i>&ycirc;(t)</i> is calculated as:</p>

  <div class="equation">
    <span class="eq-math">EoE(t) = y(t) - &ycirc;(t)</span>
    <span class="eq-num">(6)</span>
  </div>

  <p>Under nominal charging, the model prediction closely matches measured energy, keeping <i>EoE(t) &approx; 0</i>. During an FDI attack, the physical power halts while the NARX model continues forecasting positive energy, causing <i>|EoE(t)| &gg; 0</i>.</p>

  <h2 class="subsec-heading">C. Statistical IQR Bounding and Window Mechanism</h2>
  <p>Rather than using rigid static thresholds, data-driven boundaries are established via Interquartile Range (IQR) statistics on the baseline residual distribution:</p>

  <div class="equation">
    <span class="eq-math">IQR = Q<sub>3</sub> - Q<sub>1</sub></span>
    <span class="eq-num">(7)</span>
  </div>

  <div class="equation">
    <span class="eq-math">LB = Q<sub>1</sub> - &beta; &middot; IQR, &emsp; UB = Q<sub>3</sub> + &beta; &middot; IQR</span>
    <span class="eq-num">(8)</span>
  </div>

  <p>where <i>Q<sub>1</sub></i> and <i>Q<sub>3</sub></i> denote the 25th and 75th percentiles, and &beta; = 5.0 is an empirically determined scale multiplier.</p>

  <p>Routine vehicle connection/disconnection transitions and grid voltage transients create isolated single-sample residual spikes. To prevent false alarms, an attack is flagged if and only if residuals exceed bounds across <i>q = 5</i> consecutive samples:</p>

  <div class="equation">
    <span class="eq-math">Alarm(t) = 1 &emsp; if &sum;<sub>k=0</sub><sup>q-1</sup> &Iopf;(EoE(t-k) &notin; [LB, UB]) = q</span>
    <span class="eq-num">(9)</span>
  </div>

  <h1 class="sec-heading">IV. Experimental Setup & Results</h1>

  <h2 class="subsec-heading">A. Caltech ACN Dataset</h2>
  <p>The framework was evaluated using the real-world Caltech Adaptive Charging Network (ACN-Data) benchmark [7], recorded from 54 EVSEs and an 80-port garage over two months (Dec 1, 2020 &ndash; Jan 31, 2021). The final preprocessed dataset contains 47,095 samples from 169 charging sessions across 27 users and 19 EVSE units:</p>
  <ul>
    <li><b>Training Set:</b> 32,966 samples (70% train, 15% validation, 15% test).</li>
    <li><b>Evaluation Set:</b> 14,129 unseen samples under nominal and attack conditions.</li>
  </ul>

  <div class="table-title">TABLE I: Performance Comparison on Caltech ACN Dataset</div>
  <table class="ieee-table">
    <thead>
      <tr>
        <th>Performance Metric</th>
        <th>Proposed NARX</th>
        <th>FNN Model</th>
        <th>LSTM Classifier [9]</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Accuracy (%)</b></td>
        <td><b>99.40%</b></td>
        <td>88.68%</td>
        <td>98.00%</td>
      </tr>
      <tr>
        <td><b>Precision (%)</b></td>
        <td><b>74.50%</b></td>
        <td>10.90%</td>
        <td>0.00%</td>
      </tr>
      <tr>
        <td><b>Recall (%)</b></td>
        <td><b>97.50%</b></td>
        <td><b>97.50%</b></td>
        <td>0.00%</td>
      </tr>
      <tr>
        <td><b>F1-Score (%)</b></td>
        <td><b>84.40%</b></td>
        <td>19.60%</td>
        <td>0.00%</td>
      </tr>
      <tr class="last-row">
        <td><b>Mean Squared Error</b></td>
        <td><b>1.997 &times; 10<sup>-5</sup></b></td>
        <td>1.179 &times; 10<sup>-4</sup></td>
        <td>N/A</td>
      </tr>
    </tbody>
  </table>

  <h2 class="subsec-heading">B. Performance Comparison & Discussion</h2>
  <p>The proposed NARX model was benchmarked against an identical-dimension Feedforward Neural Network (FNN) and a state-of-the-art LSTM binary classification baseline [9], as presented in Table I and Fig. 3.</p>

  <figure>
    <img src="data:image/png;base64,{img3_b64}" alt="Comparative Performance Chart">
    <figcaption><strong>Fig. 3.</strong> Performance comparison (Accuracy, Precision, Recall, F1-Score) on the Caltech ACN evaluation dataset across the proposed NARX NN, FNN regression model, and LSTM binary classifier [9].</figcaption>
  </figure>

  <p><b>Analysis of Confusion Matrices:</b></p>
  <ul>
    <li><b>Proposed NARX NN:</b> Achieves 13,861 True Negatives (TN), 196 True Positives (TP), 67 False Positives (FP), and only 5 False Negatives (FN). The resulting F1-score is 84.40% with a precision of 74.50%.</li>
    <li><b>FNN Model:</b> Lacks temporal recurrent connections, resulting in elevated prediction variance. This inflates false alarms to <i>FP = 1,593</i>, dropping precision to 10.90% and F1-score to 19.60%.</li>
    <li><b>Failure of LSTM Classifier [9]:</b> Because attack samples constitute only 1.42% of the dataset, the LSTM classifier biases completely toward the majority class (<i>TN = 13,928, FN = 201, TP = 0, FP = 0</i>). Despite an apparent 98.00% accuracy, its precision, recall, and F1-score are exactly 0.00%. In contrast, the NARX regression model minimizes continuous MSE, ensuring unbiased anomaly detection regardless of class imbalance.</li>
  </ul>

  <h1 class="sec-heading">V. Hardware-in-the-Loop Validation</h1>
  <p>To confirm real-time execution feasibility on embedded microgrid controllers, the framework was deployed on an OPAL-RT OP4512 Real-Time Digital Simulator (RTDS) integrated with RT-LAB and MATLAB/Simulink (Fig. 4(a)).</p>

  <figure>
    <img src="data:image/png;base64,{img4_b64}" alt="OPAL-RT Setup and Scope Waveform">
    <figcaption><strong>Fig. 4.</strong> (a) OPAL-RT OP4512 hardware-in-the-loop simulation environment. (b) RTDS scope waveform showing attack injection at sample 8,000 (2h 13m 20s) and detection at sample 8,005 (2h 13m 25s) with a 5-second detection latency (<i>q</i> = 5).</figcaption>
  </figure>

  <p>The 14,129 evaluation samples were streamed to simulate sensor inputs at 1 sample per second. An FDI attack was introduced at sample point 8,000 (elapsed simulation time: 2h 13m 20s). The hardware controller triggered an attack alarm at sample 8,005 (2h 13m 25s). The observed latency was exactly 5 seconds, perfectly matching the window length <i>q = 5</i> (Fig. 4(b)), demonstrating deterministic real-time response without computational lag.</p>

  <h1 class="sec-heading">VI. Limitations & Mid-Sem Review Roadmap</h1>
  <p>Our mid-semester evaluation identified three open challenges:</p>
  <ol>
    <li><b>Micro-Burst Attacks:</b> Attacks lasting fewer than <i>q = 5</i> seconds terminate before triggering the consecutive window.</li>
    <li><b>Subtle Parameter Drift:</b> Minimal &phi; adjustments yield residual deviations that remain within [LB, UB].</li>
    <li><b>Static Parameters:</b> Heuristic choices for &beta; = 5 and <i>q</i> = 5 cannot adapt to dynamic grid volatility.</li>
  </ol>

  <h2 class="subsec-heading">Proposed Technical Extensions for Upcoming Reviews</h2>
  <ul>
    <li><b>Adaptive Dynamic IQR & Windowing:</b> We will formulate an online Bayesian update rule that continuously tunes &beta;(<i>t</i>) and <i>q(t)</i> according to localized grid variance.</li>
    <li><b>Attention-Augmented NARX (NARX-Transformer):</b> We propose incorporating lightweight self-attention mechanisms to learn spatial-temporal cross-bay correlations across adjacent EVSE units.</li>
    <li><b>Multi-Parameter Resiliency:</b> We will evaluate resilience against coordinated multi-vector attacks manipulating Energy Requested (<i>ED</i>), Start Time (<i>ST</i>), and dynamic pricing tariffs simultaneously.</li>
    <li><b>Edge AI Quantization:</b> We plan to quantize the model to 8-bit integer (INT8) representation for direct deployment on low-cost ARM Cortex-M microcontrollers inside Level 2 EVSEs.</li>
  </ul>

  <h1 class="sec-heading">VII. Conclusion</h1>
  <p>This report presented a regression-based cyber-defense framework using a NARX neural network to detect stealthy False Data Injection attacks in IoT-connected EV charging networks. By forecasting delivered energy and applying Interquartile Range thresholding with a 5-step consecutive spike window, the model avoids false alarms from normal session transitions while circumventing the severe class-imbalance failures of traditional ML classifiers. Tested on 47,095 real-world Caltech ACN samples, the framework achieved 99.40% accuracy, 74.50% precision, and an 84.40% F1-score. Hardware validation on an OPAL-RT simulator confirmed reliable detection within 5 seconds. The identified limitations will guide our upcoming work on adaptive thresholding and multi-parameter cyber-resilience.</p>

  <h1 class="sec-heading">References</h1>
  <div class="references-list">
    <div class="ref-item">[1] H. Basumatary, M. Khatua, and S. Nath, &ldquo;False Data Injection Attack Detection in EV Charging Network Using NARX Neural Network,&rdquo; <i>IEEE Trans. Transport. Electrific.</i>, vol. 11, no. 4, pp. 9686&ndash;9700, Aug. 2025.</div>
    <div class="ref-item">[2] J. Antoun, M. E. Kabir, B. Moussa, R. Atallah, and C. Assi, &ldquo;A detailed security assessment of the EV charging ecosystem,&rdquo; <i>IEEE Netw.</i>, vol. 34, no. 3, pp. 200&ndash;207, May 2020.</div>
    <div class="ref-item">[3] S. Sahoo, T. Dragicevic, and F. Blaabjerg, &ldquo;Cyber security in control of grid-tied power electronic converters&mdash;Challenges and vulnerabilities,&rdquo; <i>IEEE J. Emerg. Sel. Topics Power Electron.</i>, vol. 9, no. 5, pp. 5326&ndash;5340, May 2021.</div>
    <div class="ref-item">[4] F. Nejabatkhah, Y. W. Li, H. Liang, and R. Reza Ahrabi, &ldquo;Cyber-security of smart microgrids: A survey,&rdquo; <i>Energies</i>, vol. 14, no. 1, p. 27, 2021.</div>
    <div class="ref-item">[5] M. R. Habibi, H. R. Baghaee, T. Dragicevic, and F. Blaabjerg, &ldquo;Detection of false data injection cyber-attacks in DC microgrids based on recurrent neural networks,&rdquo; <i>IEEE J. Emerg. Sel. Topics Power Electron.</i>, vol. 9, no. 5, pp. 5294&ndash;5310, Oct. 2021.</div>
    <div class="ref-item">[6] M. ElKashlan, M. S. Elsayed, A. D. Jurcut, and M. Azer, &ldquo;A machine learning-based intrusion detection system for IoT electric vehicle charging stations (EVCSs),&rdquo; <i>Electronics</i>, vol. 12, no. 4, p. 1044, Feb. 2023.</div>
    <div class="ref-item">[7] Z. J. Lee, T. Li, and S. H. Low, &ldquo;ACN-data: Analysis and applications of an open EV charging dataset,&rdquo; in <i>Proc. 10th ACM Int. Conf. Future Energy Syst. (e-Energy)</i>, 2019, pp. 139&ndash;149.</div>
    <div class="ref-item">[8] H. Jahangir, S. Lakshminarayana, and H. V. Poor, &ldquo;Charge manipulation attacks against smart electric vehicle charging stations and deep learning-based detection mechanisms,&rdquo; <i>IEEE Trans. Smart Grid</i>, vol. 15, no. 5, pp. 5182&ndash;5194, Sep. 2024.</div>
    <div class="ref-item">[9] M. Basnet and M. H. Ali, &ldquo;Deep learning-based intrusion detection system for electric vehicle charging station,&rdquo; in <i>Proc. IEEE 2nd Int. Conf. Smart Power Internet Energy Syst. (SPIES)</i>, 2020, pp. 408&ndash;413.</div>
    <div class="ref-item">[10] A. A. Shafee, M. M. E. A. Mahmoud, G. Srivastava, M. M. Fouda, M. Alsabaan, and M. I. Ibrahem, &ldquo;Detection of distributed denial of charge (DDoC) attacks using deep neural networks with vector embedding,&rdquo; <i>IEEE Access</i>, vol. 11, pp. 75381&ndash;75397, 2023.</div>
    <div class="ref-item">[11] C. Alcaraz, J. Lopez, and S. Wolthusen, &ldquo;OCPP protocol: Security threats and challenges,&rdquo; <i>IEEE Trans. Smart Grid</i>, vol. 8, no. 5, pp. 2452&ndash;2459, Sep. 2017.</div>
    <div class="ref-item">[12] H. T. Siegelmann, B. G. Horne, and C. L. Giles, &ldquo;Computational capabilities of recurrent NARX neural networks,&rdquo; <i>IEEE Trans. Syst., Man, Cybern. B, Cybern.</i>, vol. 27, no. 2, pp. 208&ndash;215, Apr. 1997.</div>
  </div>

</div>

</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"IEEE HTML file written at: {html_path}")

# 4. Compile HTML to PDF using Headless Edge
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]

print("Compiling PDF with Microsoft Edge headless...")
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_path):
    print(f"SUCCESS: PDF generated at: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
else:
    print(f"ERROR: PDF generation failed. Return code: {res.returncode}")
    print("Stderr:", res.stderr)
