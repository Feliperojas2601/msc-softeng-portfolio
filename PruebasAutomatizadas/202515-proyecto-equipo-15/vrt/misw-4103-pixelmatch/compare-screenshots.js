import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import { PNG } from 'pngjs';
import pixelmatch from 'pixelmatch';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const config = JSON.parse(fs.readFileSync('./vrt.config.json', 'utf8'));

const THRESHOLD = config.threshold || 0.1;

const BASE_DIR = './screenshots-vrt-base';
const RELEASE_DIR = './screenshots-vrt-release';
const REPORT_DIR = './vrt-report';
const DIFF_DIR = path.join(REPORT_DIR, 'diff-images');

if (!fs.existsSync(REPORT_DIR)) {
    fs.mkdirSync(REPORT_DIR, { recursive: true });
}
if (!fs.existsSync(DIFF_DIR)) {
    fs.mkdirSync(DIFF_DIR, { recursive: true });
}

function getImagesRecursive(dir, baseDir = dir, images = []) {
    if (!fs.existsSync(dir)) {
        return images;
    }
    const items = fs.readdirSync(dir);
    items.forEach(item => {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            getImagesRecursive(fullPath, baseDir, images);
        } else if (item.toLowerCase().endsWith('.png')) {
            const relativePath = path.relative(baseDir, fullPath);
            images.push(relativePath);
        }
    });

    return images;
}

async function compareScreenshots(basePath, releasePath, diffPath) {
    try {
        const startTime = Date.now();
        const baseImage = PNG.sync.read(fs.readFileSync(basePath));
        const releaseImage = PNG.sync.read(fs.readFileSync(releasePath));
        const { width: baseWidth, height: baseHeight } = baseImage;
        const { width: releaseWidth, height: releaseHeight } = releaseImage;
        const isSameDimensions = baseWidth === releaseWidth && baseHeight === releaseHeight;
        let finalBaseImage = baseImage;
        let finalReleaseImage = releaseImage;
        let comparisonWidth = baseWidth;
        let comparisonHeight = baseHeight;
        if (!isSameDimensions) {
            console.log(`   ⚠️  Dimensiones diferentes detectadas: Base ${baseWidth}x${baseHeight} vs Release ${releaseWidth}x${releaseHeight}`);
            console.log(`   📐 Redimensionando a dimensiones mínimas para comparación...`);
            comparisonWidth = Math.min(baseWidth, releaseWidth);
            comparisonHeight = Math.min(baseHeight, releaseHeight);
            if (baseWidth !== comparisonWidth || baseHeight !== comparisonHeight) {
                const resizedBase = new PNG({ width: comparisonWidth, height: comparisonHeight });
                PNG.bitblt(baseImage, resizedBase, 0, 0, comparisonWidth, comparisonHeight, 0, 0);
                finalBaseImage = resizedBase;
            }
            if (releaseWidth !== comparisonWidth || releaseHeight !== comparisonHeight) {
                const resizedRelease = new PNG({ width: comparisonWidth, height: comparisonHeight });
                PNG.bitblt(releaseImage, resizedRelease, 0, 0, comparisonWidth, comparisonHeight, 0, 0);
                finalReleaseImage = resizedRelease;
            }
        }
        const diff = new PNG({ width: comparisonWidth, height: comparisonHeight });
        const numDiffPixels = pixelmatch(
            finalBaseImage.data,
            finalReleaseImage.data,
            diff.data,
            comparisonWidth,
            comparisonHeight,
            { threshold: config.threshold || 0.1 }
        );
        fs.writeFileSync(diffPath, PNG.sync.write(diff));
        const totalPixels = comparisonWidth * comparisonHeight;
        const misMatchPercentage = (numDiffPixels / totalPixels) * 100;
        const analysisTime = Date.now() - startTime;
        return {
            isSameDimensions: isSameDimensions,
            dimensionDifference: { 
                width: Math.abs(baseWidth - releaseWidth), 
                height: Math.abs(baseHeight - releaseHeight) 
            },
            baseDimensions: { width: baseWidth, height: baseHeight },
            releaseDimensions: { width: releaseWidth, height: releaseHeight },
            comparisonDimensions: { width: comparisonWidth, height: comparisonHeight },
            rawMisMatchPercentage: misMatchPercentage,
            misMatchPercentage: misMatchPercentage,
            diffPixels: numDiffPixels,
            totalPixels: totalPixels,
            analysisTime: analysisTime,
            passed: misMatchPercentage <= (THRESHOLD * 100)
        };
    } catch (error) {
        console.error(`Error comparing images: ${error.message}`);
        return {
            error: error.message,
            passed: false,
            analysisTime: 0
        };
    }
}

function generateHTMLReport(results) {
    const totalTests = results.length;
    const passedTests = results.filter(r => r.passed).length;
    const failedTests = totalTests - passedTests;
    const passRate = ((passedTests / totalTests) * 100).toFixed(2);
    const overallPassed = failedTests === 0;
    const thresholdPercentage = (THRESHOLD * 100).toFixed(1);

    const html = `
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VRT Report - PixelMatch</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f7fa;
            color: #2d3748;
            padding: 20px;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .tool-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 10px;
            font-weight: 600;
        }
        
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f7fafc;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .summary-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
            border-left: 4px solid;
        }
        
        .summary-card.overall {
            border-left-color: ${overallPassed ? '#48bb78' : '#f56565'};
        }
        
        .summary-card.passed {
            border-left-color: #48bb78;
        }
        
        .summary-card.failed {
            border-left-color: #f56565;
        }
        
        .summary-card.rate {
            border-left-color: #4299e1;
        }
        
        .summary-card.threshold {
            border-left-color: #ed8936;
        }
        
        .summary-value {
            font-size: 2.5em;
            font-weight: 700;
            margin: 10px 0;
        }
        
        .summary-label {
            color: #718096;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .overall-result {
            padding: 30px 40px;
            text-align: center;
            font-size: 1.5em;
            font-weight: 600;
            background: ${overallPassed ? '#f0fff4' : '#fff5f5'};
            color: ${overallPassed ? '#22543d' : '#742a2a'};
            border-left: 5px solid ${overallPassed ? '#48bb78' : '#f56565'};
        }
        
        .overall-result .icon {
            font-size: 2em;
            margin-right: 15px;
        }
        
        .results {
            padding: 40px;
        }
        
        .result-item {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin-bottom: 30px;
            overflow: hidden;
            transition: box-shadow 0.3s;
        }
        
        .result-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .result-header {
            padding: 20px;
            background: #f7fafc;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .result-title {
            font-size: 1.2em;
            font-weight: 600;
            color: #2d3748;
        }
        
        .result-badge {
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .result-badge.pass {
            background: #c6f6d5;
            color: #22543d;
        }
        
        .result-badge.fail {
            background: #fed7d7;
            color: #742a2a;
        }
        
        .result-content {
            padding: 20px;
        }
        
        .result-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat {
            padding: 12px;
            background: #f7fafc;
            border-radius: 6px;
        }
        
        .stat-label {
            font-size: 0.85em;
            color: #718096;
            margin-bottom: 4px;
        }
        
        .stat-value {
            font-size: 1.1em;
            font-weight: 600;
            color: #2d3748;
        }
        
        .images-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .image-container {
            text-align: center;
        }
        
        .image-label {
            font-size: 0.9em;
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 10px;
            padding: 8px;
            background: #edf2f7;
            border-radius: 4px;
        }
        
        .image-container img {
            width: 100%;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .footer {
            padding: 30px 40px;
            background: #2d3748;
            color: white;
            text-align: center;
        }
        
        .footer p {
            margin: 5px 0;
        }
        
        .error-message {
            padding: 15px;
            background: #fff5f5;
            border-left: 4px solid #f56565;
            color: #742a2a;
            border-radius: 4px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 VRT Report Pixelmatch</h1>
            <p>Comparación de screenshots entre Ghost 4.5.0 (Base) y versión Release</p>
        </div>
        
        <div class="summary">
            <div class="summary-card overall">
                <div class="summary-label">Estado General</div>
                <div class="summary-value">${overallPassed ? '✅ PASS' : '❌ FAIL'}</div>
            </div>
            <div class="summary-card passed">
                <div class="summary-label">Pruebas Exitosas</div>
                <div class="summary-value">${passedTests}</div>
            </div>
            <div class="summary-card failed">
                <div class="summary-label">Pruebas Fallidas</div>
                <div class="summary-value">${failedTests}</div>
            </div>
            <div class="summary-card rate">
                <div class="summary-label">Tasa de Éxito</div>
                <div class="summary-value">${passRate}%</div>
            </div>
            <div class="summary-card threshold">
                <div class="summary-label">Threshold</div>
                <div class="summary-value">${thresholdPercentage}%</div>
            </div>
        </div>
        
        <div class="overall-result">
            <span class="icon">${overallPassed ? '✅' : '❌'}</span>
            ${overallPassed 
                ? 'Todas las pruebas VRT han pasado exitosamente' 
                : `${failedTests} prueba(s) excedieron el threshold de ${thresholdPercentage}%`
            }
        </div>
        
        <div class="results">
            <h2 style="margin-bottom: 30px; color: #2d3748;">Resultados Detallados (${totalTests} comparaciones)</h2>
            ${results.map((result, index) => `
                <div class="result-item">
                    <div class="result-header">
                        <div class="result-title">${result.path}</div>
                        <div class="result-badge ${result.passed ? 'pass' : 'fail'}">
                            ${result.passed ? 'PASS' : 'FAIL'}
                        </div>
                    </div>
                    <div class="result-content">
                        ${result.error ? `
                            <div class="error-message">
                                <strong>Error:</strong> ${result.error}
                            </div>
                        ` : `
                            <div class="result-stats">
                                <div class="stat">
                                    <div class="stat-label">Diferencia</div>
                                    <div class="stat-value" style="color: ${result.passed ? '#48bb78' : '#f56565'}">
                                        ${result.misMatchPercentage.toFixed(2)}%
                                    </div>
                                </div>
                                <div class="stat">
                                    <div class="stat-label">Píxeles Diferentes</div>
                                    <div class="stat-value">${result.diffPixels ? result.diffPixels.toLocaleString() : 'N/A'}</div>
                                </div>
                                <div class="stat">
                                    <div class="stat-label">Total Píxeles</div>
                                    <div class="stat-value">${result.totalPixels ? result.totalPixels.toLocaleString() : 'N/A'}</div>
                                </div>
                                <div class="stat">
                                    <div class="stat-label">Dimensiones Base</div>
                                    <div class="stat-value">${result.baseDimensions ? `${result.baseDimensions.width}x${result.baseDimensions.height}` : 'N/A'}</div>
                                </div>
                                <div class="stat">
                                    <div class="stat-label">Dimensiones Release</div>
                                    <div class="stat-value">${result.releaseDimensions ? `${result.releaseDimensions.width}x${result.releaseDimensions.height}` : 'N/A'}</div>
                                </div>
                                ${!result.isSameDimensions ? `
                                    <div class="stat">
                                        <div class="stat-label">Comparación en</div>
                                        <div class="stat-value" style="color: #ed8936;">
                                            ${result.comparisonDimensions.width}x${result.comparisonDimensions.height}
                                        </div>
                                    </div>
                                ` : ''}
                                <div class="stat">
                                    <div class="stat-label">Tiempo de Análisis</div>
                                    <div class="stat-value">${result.analysisTime}ms</div>
                                </div>
                                ${!result.isSameDimensions ? `
                                    <div class="stat" style="grid-column: 1 / -1; background: #fff5f5; border-left: 3px solid #ed8936;">
                                        <div class="stat-label" style="color: #c05621;">⚠️ Advertencia de Dimensiones</div>
                                        <div class="stat-value" style="font-size: 0.9em; color: #742a2a;">
                                            Las imágenes tienen dimensiones diferentes. Comparación realizada en área común: ${result.comparisonDimensions.width}x${result.comparisonDimensions.height}
                                        </div>
                                    </div>
                                ` : ''}
                            </div>
                            
                            <div class="images-grid">
                                <div class="image-container">
                                    <div class="image-label">📸 Base (Ghost 4.5.0)</div>
                                    <img src="../${BASE_DIR}/${result.path}" alt="Base">
                                </div>
                                <div class="image-container">
                                    <div class="image-label">📸 Release</div>
                                    <img src="../${RELEASE_DIR}/${result.path}" alt="Release">
                                </div>
                                <div class="image-container">
                                    <div class="image-label">🔍 Diferencias (PixelMatch)</div>
                                    <img src="./diff-images/${result.diffImageName}" alt="Diff">
                                </div>
                            </div>
                        `}
                    </div>
                </div>
            `).join('')}
        </div>
        
        <div class="footer">
            <p><strong>🔍 Herramienta:</strong> PixelMatch (Comparación pixel a pixel)</p>
            <p><strong>Generado:</strong> ${new Date().toLocaleString('es-ES')}</p>
            <p><strong>Threshold Configurado:</strong> ${thresholdPercentage}% (Las imágenes con diferencia ≤ ${thresholdPercentage}% se consideran PASS)</p>
            <p><strong>Total de Comparaciones:</strong> ${totalTests}</p>
        </div>
    </div>
</body>
</html>
    `;

    return html;
}

async function runVRT() {
    console.log('🚀 Iniciando Visual Regression Testing con PixelMatch...\n');
    console.log(`📊 Threshold configurado: ${(THRESHOLD * 100).toFixed(1)}%`);
    console.log(`   (Diferencias ≤ ${(THRESHOLD * 100).toFixed(1)}% = PASS, > ${(THRESHOLD * 100).toFixed(1)}% = FAIL)\n`);
    
    const baseImages = getImagesRecursive(BASE_DIR, BASE_DIR);
    console.log(`📁 Imágenes encontradas en Base: ${baseImages.length}`);
    
    const imagesToCompare = baseImages.filter(imagePath => {
        const releasePath = path.join(RELEASE_DIR, imagePath);
        return fs.existsSync(releasePath);
    });
    
    console.log(`✅ Imágenes coincidentes para comparar: ${imagesToCompare.length}`);
    
    if (baseImages.length > imagesToCompare.length) {
        console.log(`⚠️  ${baseImages.length - imagesToCompare.length} imagen(es) solo existen en Base y serán omitidas\n`);
    }
    
    if (imagesToCompare.length === 0) {
        console.log('❌ No se encontraron imágenes coincidentes para comparar');
        return;
    }
    
    const results = [];
    
    for (let i = 0; i < imagesToCompare.length; i++) {
        const imagePath = imagesToCompare[i];
        const basePath = path.join(BASE_DIR, imagePath);
        const releasePath = path.join(RELEASE_DIR, imagePath);
        const diffImageName = `diff-${i + 1}-${path.basename(imagePath)}`;
        const diffPath = path.join(DIFF_DIR, diffImageName);
        
        console.log(`🔍 Comparando [${i + 1}/${imagesToCompare.length}]: ${imagePath}`);
        
        const comparisonResult = await compareScreenshots(basePath, releasePath, diffPath);
        
        const result = {
            path: imagePath,
            diffImageName,
            ...comparisonResult
        };
        
        results.push(result);
        
        const status = result.passed ? '✅ PASS' : '❌ FAIL';
        const percentage = result.error ? 'ERROR' : `${result.misMatchPercentage.toFixed(2)}%`;
        const pixels = result.diffPixels ? ` (${result.diffPixels.toLocaleString()} píxeles)` : '';
        console.log(`   ${status} - Diferencia: ${percentage}${pixels}\n`);
    }
    
    console.log('📝 Generando reporte HTML...');
    const htmlReport = generateHTMLReport(results);
    const reportPath = path.join(REPORT_DIR, 'index.html');
    fs.writeFileSync(reportPath, htmlReport);
    
    const passedCount = results.filter(r => r.passed).length;
    const failedCount = results.length - passedCount;
    const overallPassed = failedCount === 0;
    
    console.log('\n' + '='.repeat(60));
    console.log('📊 RESUMEN FINAL - PixelMatch');
    console.log('='.repeat(60));
    console.log(`Total de comparaciones: ${results.length}`);
    console.log(`✅ Pruebas exitosas: ${passedCount}`);
    console.log(`❌ Pruebas fallidas: ${failedCount}`);
    console.log(`📈 Tasa de éxito: ${((passedCount / results.length) * 100).toFixed(2)}%`);
    console.log(`🎯 Threshold: ${(THRESHOLD * 100).toFixed(1)}%`);
    console.log('⬆️ Diferencia máxima encontrada: ' +
        `${results.reduce((max, r) => r.misMatchPercentage > max ? r.misMatchPercentage : max, 0).toFixed(2)}%`);
    console.log('='.repeat(60));
    console.log(`\n${overallPassed ? '✅ RESULTADO: PASS' : '❌ RESULTADO: FAIL'}`);
    console.log(`\n📄 Reporte generado en: ${reportPath}`);
    console.log(`🖼️  Imágenes de diferencia en: ${DIFF_DIR}\n`);
    console.log('🚀 Visual Regression Testing completado.\n');
    
    process.exit(0);
}

runVRT().catch(error => {
    console.error('❌ Error fatal:', error);
    process.exit(1);
});
