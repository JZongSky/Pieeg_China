// PIEEG 交互式图表库
// 包含EEG波形图、频谱分析图、产品对比图等可视化组件

// 全局配置
const CHART_COLORS = {
  primary: '#1A365D',
  secondary: '#00B4D8',
  accent: '#FF7D00',
  delta: '#4361EE',
  theta: '#3A0CA3',
  alpha: '#7209B7',
  beta: '#F72585',
  gamma: '#4CC9F0',
  gray: '#333333',
  lightGray: '#F5F7FA',
  white: '#FFFFFF'
};

// 加载数据
async function loadEEGData() {
  try {
    const response = await fetch('/static/data/sample_eeg_data.json');
    return await response.json();
  } catch (error) {
    console.error('加载EEG数据失败:', error);
    return null;
  }
}

// EEG波形图
function createEEGWaveformChart(containerId, channelName = 'Fp1') {
  loadEEGData().then(data => {
    if (!data) return;
    
    const eegData = data.eeg_data;
    const timeData = eegData.time;
    const channelData = eegData.data[channelName];
    
    const trace = {
      x: timeData,
      y: channelData,
      type: 'scatter',
      mode: 'lines',
      name: channelName,
      line: {
        color: CHART_COLORS.secondary,
        width: 2
      }
    };
    
    const layout = {
      title: `EEG波形图 - ${channelName}通道`,
      font: {
        family: 'Arial, sans-serif',
        size: 14
      },
      plot_bgcolor: CHART_COLORS.lightGray,
      paper_bgcolor: CHART_COLORS.white,
      xaxis: {
        title: '时间 (秒)',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      yaxis: {
        title: '振幅 (μV)',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      margin: {
        l: 50,
        r: 20,
        t: 50,
        b: 50
      },
      hovermode: 'closest',
      showlegend: true
    };
    
    const config = {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['lasso2d', 'select2d'],
      displaylogo: false
    };
    
    Plotly.newPlot(containerId, [trace], layout, config);
  });
}

// 多通道EEG波形图
function createMultiChannelEEGChart(containerId, channels = ['Fp1', 'Fp2', 'F3', 'F4']) {
  loadEEGData().then(data => {
    if (!data) return;
    
    const eegData = data.eeg_data;
    const timeData = eegData.time;
    const traces = [];
    
    // 计算偏移量，使通道显示分开
    const offset = 20;
    
    channels.forEach((channel, index) => {
      const channelData = eegData.data[channel].map(val => val + (index * offset));
      
      traces.push({
        x: timeData,
        y: channelData,
        type: 'scatter',
        mode: 'lines',
        name: channel,
        line: {
          width: 1.5
        }
      });
    });
    
    const layout = {
      title: '多通道EEG波形图',
      font: {
        family: 'Arial, sans-serif',
        size: 14
      },
      plot_bgcolor: CHART_COLORS.lightGray,
      paper_bgcolor: CHART_COLORS.white,
      xaxis: {
        title: '时间 (秒)',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      yaxis: {
        title: '振幅 (μV) + 偏移',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      margin: {
        l: 50,
        r: 20,
        t: 50,
        b: 50
      },
      hovermode: 'closest',
      showlegend: true
    };
    
    const config = {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['lasso2d', 'select2d'],
      displaylogo: false
    };
    
    Plotly.newPlot(containerId, traces, layout, config);
  });
}

// 频谱分析图
function createSpectralAnalysisChart(containerId, channelName = 'O1') {
  loadEEGData().then(data => {
    if (!data) return;
    
    const spectralData = data.spectral_data;
    const frequencies = spectralData.frequencies;
    const powerData = spectralData.power[channelName];
    const bands = data.frequency_bands;
    
    // 主要频谱数据
    const trace = {
      x: frequencies,
      y: powerData,
      type: 'scatter',
      mode: 'lines',
      name: `${channelName} 功率谱`,
      line: {
        color: CHART_COLORS.primary,
        width: 2
      }
    };
    
    // 频带区域
    const bandTraces = [];
    const bandColors = {
      delta: CHART_COLORS.delta,
      theta: CHART_COLORS.theta,
      alpha: CHART_COLORS.alpha,
      beta: CHART_COLORS.beta,
      gamma: CHART_COLORS.gamma
    };
    
    Object.entries(bands).forEach(([bandName, [min, max]]) => {
      // 找到频率范围内的索引
      const startIdx = frequencies.findIndex(f => f >= min);
      const endIdx = frequencies.findIndex(f => f >= max) - 1;
      
      if (startIdx >= 0 && endIdx >= 0) {
        const bandFreqs = frequencies.slice(startIdx, endIdx + 1);
        const bandPower = powerData.slice(startIdx, endIdx + 1);
        
        bandTraces.push({
          x: bandFreqs,
          y: bandPower,
          type: 'scatter',
          mode: 'lines',
          name: `${bandName} (${min}-${max} Hz)`,
          fill: 'tozeroy',
          line: {
            color: bandColors[bandName],
            width: 0
          },
          fillcolor: `${bandColors[bandName]}40` // 40 = 25% opacity
        });
      }
    });
    
    const layout = {
      title: `频谱分析 - ${channelName}通道`,
      font: {
        family: 'Arial, sans-serif',
        size: 14
      },
      plot_bgcolor: CHART_COLORS.lightGray,
      paper_bgcolor: CHART_COLORS.white,
      xaxis: {
        title: '频率 (Hz)',
        type: 'log',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      yaxis: {
        title: '功率 (μV²/Hz)',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      margin: {
        l: 50,
        r: 20,
        t: 50,
        b: 50
      },
      hovermode: 'closest',
      showlegend: true
    };
    
    const config = {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['lasso2d', 'select2d'],
      displaylogo: false
    };
    
    Plotly.newPlot(containerId, [trace, ...bandTraces], layout, config);
  });
}

// 产品对比雷达图
function createProductComparisonChart(containerId) {
  loadEEGData().then(data => {
    if (!data) return;
    
    const comparisonData = data.product_comparison;
    const products = comparisonData.products;
    const features = comparisonData.features;
    
    // 标准化特征值，使其在0-1之间
    const normalizedFeatures = {};
    Object.entries(features).forEach(([feature, values]) => {
      const max = Math.max(...values);
      normalizedFeatures[feature] = values.map(val => val / max);
    });
    
    // 雷达图的特征名称
    const featureNames = Object.keys(features);
    
    // 为每个产品创建一个trace
    const traces = products.map((product, idx) => {
      const values = featureNames.map(feature => {
        return normalizedFeatures[feature][idx];
      });
      
      // 闭合雷达图
      values.push(values[0]);
      const labels = [...featureNames, featureNames[0]];
      
      return {
        type: 'scatterpolar',
        name: product,
        r: values,
        theta: labels,
        fill: 'toself',
        opacity: 0.7
      };
    });
    
    const layout = {
      title: 'PIEEG产品对比',
      font: {
        family: 'Arial, sans-serif',
        size: 14
      },
      polar: {
        radialaxis: {
          visible: true,
          range: [0, 1]
        }
      },
      showlegend: true,
      margin: {
        l: 50,
        r: 50,
        t: 50,
        b: 50
      },
      paper_bgcolor: CHART_COLORS.white
    };
    
    const config = {
      responsive: true,
      displayModeBar: false,
      displaylogo: false
    };
    
    Plotly.newPlot(containerId, traces, layout, config);
  });
}

// EMG波形图
function createEMGWaveformChart(containerId) {
  loadEEGData().then(data => {
    if (!data) return;
    
    const emgData = data.emg_data;
    
    const trace = {
      x: emgData.time,
      y: emgData.data,
      type: 'scatter',
      mode: 'lines',
      name: 'EMG',
      line: {
        color: CHART_COLORS.accent,
        width: 2
      }
    };
    
    const layout = {
      title: 'EMG波形图',
      font: {
        family: 'Arial, sans-serif',
        size: 14
      },
      plot_bgcolor: CHART_COLORS.lightGray,
      paper_bgcolor: CHART_COLORS.white,
      xaxis: {
        title: '时间 (秒)',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      yaxis: {
        title: '振幅 (μV)',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      margin: {
        l: 50,
        r: 20,
        t: 50,
        b: 50
      },
      hovermode: 'closest',
      showlegend: true
    };
    
    const config = {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['lasso2d', 'select2d'],
      displaylogo: false
    };
    
    Plotly.newPlot(containerId, [trace], layout, config);
  });
}

// ECG波形图
function createECGWaveformChart(containerId) {
  loadEEGData().then(data => {
    if (!data) return;
    
    const ecgData = data.ecg_data;
    
    const trace = {
      x: ecgData.time,
      y: ecgData.data,
      type: 'scatter',
      mode: 'lines',
      name: 'ECG',
      line: {
        color: '#E63946',
        width: 2
      }
    };
    
    const layout = {
      title: 'ECG波形图',
      font: {
        family: 'Arial, sans-serif',
        size: 14
      },
      plot_bgcolor: CHART_COLORS.lightGray,
      paper_bgcolor: CHART_COLORS.white,
      xaxis: {
        title: '时间 (秒)',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      yaxis: {
        title: '振幅 (μV)',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      margin: {
        l: 50,
        r: 20,
        t: 50,
        b: 50
      },
      hovermode: 'closest',
      showlegend: true
    };
    
    const config = {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['lasso2d', 'select2d'],
      displaylogo: false
    };
    
    Plotly.newPlot(containerId, [trace], layout, config);
  });
}

// 3D脑地形图
function create3DBrainTopoMap(containerId) {
  loadEEGData().then(data => {
    if (!data) return;
    
    // 创建电极位置数据
    const electrodes = data.eeg_data.channels;
    
    // 简化的电极坐标 (x, y, z)
    const positions = {
      'Fp1': [-0.3, 0.9, 0],
      'Fp2': [0.3, 0.9, 0],
      'F7': [-0.7, 0.5, 0],
      'F3': [-0.3, 0.5, 0],
      'F4': [0.3, 0.5, 0],
      'F8': [0.7, 0.5, 0],
      'T3': [-0.9, 0, 0],
      'C3': [-0.5, 0, 0],
      'C4': [0.5, 0, 0],
      'T4': [0.9, 0, 0],
      'T5': [-0.7, -0.5, 0],
      'P3': [-0.3, -0.5, 0],
      'P4': [0.3, -0.5, 0],
      'T6': [0.7, -0.5, 0],
      'O1': [-0.3, -0.9, 0],
      'O2': [0.3, -0.9, 0]
    };
    
    // 从频谱数据中获取alpha波段的功率作为z值
    const alphaIdx = data.spectral_data.frequencies.findIndex(f => f >= 10) - 1;
    const zValues = electrodes.map(e => data.spectral_data.power[e][alphaIdx]);
    const maxZ = Math.max(...zValues);
    
    // 创建电极点
    const electrodeTrace = {
      x: electrodes.map(e => positions[e][0]),
      y: electrodes.map(e => positions[e][1]),
      z: zValues.map(z => z / maxZ), // 标准化
      mode: 'markers+text',
      type: 'scatter3d',
      marker: {
        size: 8,
        color: zValues,
        colorscale: 'Viridis',
        opacity: 0.8
      },
      text: electrodes,
      textposition: 'top center',
      name: '电极'
    };
    
    // 创建插值表面
    const gridSize = 20;
    const x = Array.from({length: gridSize}, (_, i) => -1 + (i * 2 / (gridSize - 1)));
    const y = Array.from({length: gridSize}, (_, i) => -1 + (i * 2 / (gridSize - 1)));
    
    // 简单的反距离加权插值
    const z = Array(gridSize).fill().map(() => Array(gridSize).fill(0));
    
    for (let i = 0; i < gridSize; i++) {
      for (let j = 0; j < gridSize; j++) {
        let weightSum = 0;
        let valueSum = 0;
        
        // 只在椭圆内插值
        const dist = Math.sqrt(x[i]*x[i] + y[j]*y[j]);
        if (dist <= 1) {
          for (let k = 0; k < electrodes.length; k++) {
            const e = electrodes[k];
            const ex = positions[e][0];
            const ey = positions[e][1];
            const ez = zValues[k] / maxZ;
            
            const distance = Math.sqrt((x[i] - ex)**2 + (y[j] - ey)**2);
            const weight = distance < 0.001 ? 1000 : 1 / distance**2;
            
            weightSum += weight;
            valueSum += ez * weight;
          }
          z[j][i] = valueSum / weightSum;
        } else {
          z[j][i] = null; // 椭圆外不显示
        }
      }
    }
    
    const surfaceTrace = {
      x: x,
      y: y,
      z: z,
      type: 'surface',
      colorscale: 'Viridis',
      opacity: 0.8,
      showscale: false,
      contours: {
        z: {
          show: true,
          usecolormap: true,
          highlightcolor: "#42f5ef",
          project: {z: true}
        }
      }
    };
    
    const layout = {
      title: '脑电地形图 (Alpha波段)',
      font: {
        family: 'Arial, sans-serif',
        size: 14
      },
      scene: {
        xaxis: {
          showgrid: false,
          zeroline: false,
          showticklabels: false
        },
        yaxis: {
          showgrid: false,
          zeroline: false,
          showticklabels: false
        },
        zaxis: {
          showgrid: false,
          zeroline: false,
          showticklabels: false
        },
        camera: {
          eye: {x: 0, y: 0, z: 2}
        },
        aspectratio: {x: 1, y: 1, z: 0.5}
      },
      margin: {
        l: 0,
        r: 0,
        t: 50,
        b: 0
      },
      paper_bgcolor: CHART_COLORS.white
    };
    
    const config = {
      responsive: true,
      displayModeBar: true,
      displaylogo: false
    };
    
    Plotly.newPlot(containerId, [surfaceTrace, electrodeTrace], layout, config);
  });
}

// 频带能量柱状图
function createFrequencyBandBarChart(containerId, channelName = 'O1') {
  loadEEGData().then(data => {
    if (!data) return;
    
    const spectralData = data.spectral_data;
    const frequencies = spectralData.frequencies;
    const powerData = spectralData.power[channelName];
    const bands = data.frequency_bands;
    
    // 计算每个频带的平均能量
    const bandEnergies = {};
    Object.entries(bands).forEach(([bandName, [min, max]]) => {
      // 找到频率范围内的索引
      const startIdx = frequencies.findIndex(f => f >= min);
      const endIdx = frequencies.findIndex(f => f >= max) - 1;
      
      if (startIdx >= 0 && endIdx >= 0) {
        const bandPower = powerData.slice(startIdx, endIdx + 1);
        bandEnergies[bandName] = bandPower.reduce((sum, val) => sum + val, 0) / bandPower.length;
      } else {
        bandEnergies[bandName] = 0;
      }
    });
    
    const bandColors = {
      delta: CHART_COLORS.delta,
      theta: CHART_COLORS.theta,
      alpha: CHART_COLORS.alpha,
      beta: CHART_COLORS.beta,
      gamma: CHART_COLORS.gamma
    };
    
    const trace = {
      x: Object.keys(bandEnergies),
      y: Object.values(bandEnergies),
      type: 'bar',
      marker: {
        color: Object.keys(bandEnergies).map(band => bandColors[band]),
        opacity: 0.8,
        line: {
          color: 'rgba(0,0,0,0.3)',
          width: 1
        }
      }
    };
    
    const layout = {
      title: `频带能量分布 - ${channelName}通道`,
      font: {
        family: 'Arial, sans-serif',
        size: 14
      },
      plot_bgcolor: CHART_COLORS.lightGray,
      paper_bgcolor: CHART_COLORS.white,
      xaxis: {
        title: '频带',
        showgrid: false
      },
      yaxis: {
        title: '平均功率 (μV²/Hz)',
        showgrid: true,
        gridcolor: 'rgba(0,0,0,0.1)'
      },
      margin: {
        l: 50,
        r: 20,
        t: 50,
        b: 50
      },
      bargap: 0.3
    };
    
    const config = {
      responsive: true,
      displayModeBar: false,
      displaylogo: false
    };
    
    Plotly.newPlot(containerId, [trace], layout, config);
  });
}

// 初始化所有图表
function initializeAllCharts() {
  // 检查容器是否存在
  const checkContainer = (id) => document.getElementById(id) !== null;
  
  // 初始化各种图表
  if (checkContainer('eeg-waveform-chart')) {
    createEEGWaveformChart('eeg-waveform-chart');
  }
  
  if (checkContainer('multi-channel-eeg-chart')) {
    createMultiChannelEEGChart('multi-channel-eeg-chart');
  }
  
  if (checkContainer('spectral-analysis-chart')) {
    createSpectralAnalysisChart('spectral-analysis-chart');
  }
  
  if (checkContainer('product-comparison-chart')) {
    createProductComparisonChart('product-comparison-chart');
  }
  
  if (checkContainer('emg-waveform-chart')) {
    createEMGWaveformChart('emg-waveform-chart');
  }
  
  if (checkContainer('ecg-waveform-chart')) {
    createECGWaveformChart('ecg-waveform-chart');
  }
  
  if (checkContainer('brain-topo-map')) {
    create3DBrainTopoMap('brain-topo-map');
  }
  
  if (checkContainer('frequency-band-chart')) {
    createFrequencyBandBarChart('frequency-band-chart');
  }
}

// 页面加载完成后初始化图表
document.addEventListener('DOMContentLoaded', initializeAllCharts);

// 导出函数供外部使用
window.PIEEG = {
  createEEGWaveformChart,
  createMultiChannelEEGChart,
  createSpectralAnalysisChart,
  createProductComparisonChart,
  createEMGWaveformChart,
  createECGWaveformChart,
  create3DBrainTopoMap,
  createFrequencyBandBarChart,
  initializeAllCharts
};
