# SmartRecon - Project Overview

## Workflow Diagram

```mermaid
flowchart TD
    Start([Start Reconciliation]) --> DC1
    
    %% Step 1: Data Collection
    subgraph DataCollection [Data Collection]
        DC1[Extract GL entries from ERP] 
        DC2[Obtain bank statements]
        DC3[Validate file formats and completeness]
    end
    
    DC1 --> DC2 --> DC3 --> DP1
    
    // ...existing mermaid code from your diagram...
```

[View Full Project Documentation](./00_Data_Recon_Project_Description_v1.html)