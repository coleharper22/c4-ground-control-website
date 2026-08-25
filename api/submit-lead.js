const https = require('https');
const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }

  try {
    const { name, email, phone, service, message } = req.body;

    // Validate required fields
    if (!name || !email || !phone || !service || !message) {
      return res.status(400).json({ 
        success: false, 
        error: 'All fields are required' 
      });
    }

    // Prepare HCP lead data
    const hcpData = JSON.stringify({
      customer: {
        first_name: name.split(' ')[0] || name,
        last_name: name.split(' ').slice(1).join(' ') || '',
        email: email,
        mobile_number: phone,
        notifications_enabled: true
      },
      source: 'Website - c4groundcontrol.com',
      service_type: service,
      description: `Service Interest: ${service}\n\nCustomer Message:\n${message}`,
      tags: [service, 'Website Lead']
    });

    // Create lead in HousecallPro
    const hcpResponse = await new Promise((resolve, reject) => {
      const options = {
        hostname: 'api.housecallpro.com',
        path: '/leads',
        method: 'POST',
        headers: {
          'Authorization': 'Token 10d6d33f386e4d0d9eba59e89313c53d',
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(hcpData)
        }
      };

      const hcpReq = https.request(options, (hcpRes) => {
        let data = '';
        
        hcpRes.on('data', (chunk) => {
          data += chunk;
        });
        
        hcpRes.on('end', () => {
          if (hcpRes.statusCode >= 200 && hcpRes.statusCode < 300) {
            resolve({ success: true, data: JSON.parse(data) });
          } else {
            reject(new Error(`HCP API error: ${hcpRes.statusCode} - ${data}`));
          }
        });
      });

      hcpReq.on('error', (error) => {
        reject(error);
      });

      hcpReq.write(hcpData);
      hcpReq.end();
    });

    // Save backup locally (Note: Vercel serverless functions have /tmp directory)
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `${name.replace(/\s+/g, '-')}-${timestamp}.json`;
    const backupDir = '/tmp/website-leads'; // Vercel temp directory
    
    // For local development, use the home directory path
    const isLocal = process.env.NODE_ENV !== 'production';
    const localBackupDir = path.join(process.env.HOME || '/Users/c4groundcontrol', 'Documents', 'C4-AI-Bot', 'Website-Leads');
    
    const targetDir = isLocal ? localBackupDir : backupDir;
    
    try {
      // Create directory if it doesn't exist
      if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
      }

      const backupData = {
        timestamp: new Date().toISOString(),
        formData: { name, email, phone, service, message },
        hcpResponse: hcpResponse.data
      };

      fs.writeFileSync(
        path.join(targetDir, filename),
        JSON.stringify(backupData, null, 2)
      );
    } catch (backupError) {
      console.error('Backup save error:', backupError);
      // Don't fail the request if backup fails
    }

    // Return success
    return res.status(200).json({
      success: true,
      message: 'Lead submitted successfully',
      customerId: hcpResponse.data.id || null
    });

  } catch (error) {
    console.error('Error processing lead:', error);
    return res.status(500).json({
      success: false,
      error: 'Failed to submit lead. Please try again or call us directly.',
      details: error.message
    });
  }
};
