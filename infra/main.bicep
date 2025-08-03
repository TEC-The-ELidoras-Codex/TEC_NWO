@description('The Elidoras Codex - Main Infrastructure Template')
@description('Deploys the complete Azure infrastructure for TEC platform')

targetScope = 'resourceGroup'

// Parameters
@description('Environment name (dev, staging, prod)')
param environmentName string = 'dev'

@description('Application name')
param applicationName string = 'elidoras-codex'

@description('Azure region for deployment')
param location string = resourceGroup().location

@description('Resource token for unique naming')
param resourceToken string = toLower(uniqueString(subscription().id, environmentName, location))

@description('Container image tag')
param containerImageTag string = 'latest'

@description('Azure OpenAI API key')
@secure()
param openAiApiKey string

@description('Administrator username for PostgreSQL')
param dbAdminUsername string = 'tecadmin'

@description('Administrator password for PostgreSQL')
@secure()
param dbAdminPassword string

// Variables
var tags = {
  Environment: environmentName
  Application: applicationName
  Project: 'TheElidorasCodex'
  ManagedBy: 'Bicep'
  'azd-env-name': environmentName
}

var resourceNames = {
  containerApp: '${applicationName}-app-${resourceToken}'
  containerAppsEnvironment: '${applicationName}-env-${resourceToken}'
  containerRegistry: 'tecregistry${resourceToken}'
  keyVault: '${applicationName}-kv-${resourceToken}'
  logAnalytics: '${applicationName}-logs-${resourceToken}'
  applicationInsights: '${applicationName}-ai-${resourceToken}'
  postgreSQL: '${applicationName}-db-${resourceToken}'
  aiSearch: '${applicationName}-search-${resourceToken}'
  storageAccount: 'tecstorage${resourceToken}'
  openAi: '${applicationName}-openai-${resourceToken}'
  managedIdentity: '${applicationName}-id-${resourceToken}'
}

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: resourceNames.logAnalytics
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: environmentName == 'prod' ? 90 : 30
    workspaceCapping: {
      dailyQuotaGb: environmentName == 'prod' ? 10 : 5
    }
  }
}

// Application Insights
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: resourceNames.applicationInsights
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// User Managed Identity
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: resourceNames.managedIdentity
  location: location
  tags: tags
}

// Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: resourceNames.keyVault
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: tenant().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    publicNetworkAccess: 'Enabled'
    accessPolicies: []
  }
}

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: resourceNames.storageAccount
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: true
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
}

// Container Registry
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: resourceNames.containerRegistry
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
    publicNetworkAccess: 'Enabled'
    networkRuleBypassOptions: 'AzureServices'
  }
}

// PostgreSQL Flexible Server
resource postgreSQL 'Microsoft.DBforPostgreSQL/flexibleServers@2023-06-01-preview' = {
  name: resourceNames.postgreSQL
  location: location
  tags: tags
  sku: {
    name: environmentName == 'prod' ? 'Standard_B2s' : 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    version: '15'
    administratorLogin: dbAdminUsername
    administratorLoginPassword: dbAdminPassword
    storage: {
      storageSizeGB: environmentName == 'prod' ? 128 : 32
    }
    backup: {
      backupRetentionDays: environmentName == 'prod' ? 35 : 7
      geoRedundantBackup: environmentName == 'prod' ? 'Enabled' : 'Disabled'
    }
    highAvailability: {
      mode: environmentName == 'prod' ? 'ZoneRedundant' : 'Disabled'
    }
    network: {
      publicNetworkAccess: 'Enabled'
    }
  }
}

// PostgreSQL Database
resource postgreSQLDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-06-01-preview' = {
  parent: postgreSQL
  name: 'tecdb'
  properties: {
    charset: 'UTF8'
    collation: 'en_US.UTF8'
  }
}

// Azure AI Search
resource aiSearch 'Microsoft.Search/searchServices@2023-11-01' = {
  name: resourceNames.aiSearch
  location: location
  tags: tags
  sku: {
    name: environmentName == 'prod' ? 'standard' : 'basic'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    networkRuleSet: {
      ipRules: []
    }
    encryptionWithCmk: {
      enforcement: 'Unspecified'
    }
    disableLocalAuth: false
    authOptions: {
      apiKeyOnly: {}
    }
  }
}

// Container Apps Environment
resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: resourceNames.containerAppsEnvironment
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
    zoneRedundant: environmentName == 'prod' ? true : false
  }
}

// Container App
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: resourceNames.containerApp
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 3000
        allowInsecure: false
        traffic: [
          {
            weight: 100
            latestRevision: true
          }
        ]
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
          allowedHeaders: ['*']
          allowCredentials: true
        }
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: managedIdentity.id
        }
      ]
      secrets: [
        {
          name: 'openai-api-key'
          value: openAiApiKey
        }
        {
          name: 'db-connection-string'
          value: 'postgresql://${dbAdminUsername}:${dbAdminPassword}@${postgreSQL.properties.fullyQualifiedDomainName}:5432/tecdb'
        }
        {
          name: 'ai-search-key'
          value: aiSearch.listAdminKeys().primaryKey
        }
      ]
    }
    template: {
      containers: [
        {
          image: '${containerRegistry.properties.loginServer}/elidoras-codex:${containerImageTag}'
          name: 'elidoras-codex'
          resources: {
            cpu: json(environmentName == 'prod' ? '1.0' : '0.5')
            memory: environmentName == 'prod' ? '2Gi' : '1Gi'
          }
          env: [
            {
              name: 'NODE_ENV'
              value: environmentName
            }
            {
              name: 'PORT'
              value: '3000'
            }
            {
              name: 'AZURE_CLIENT_ID'
              value: managedIdentity.properties.clientId
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: applicationInsights.properties.ConnectionString
            }
            {
              name: 'OPENAI_API_KEY'
              secretRef: 'openai-api-key'
            }
            {
              name: 'DATABASE_URL'
              secretRef: 'db-connection-string'
            }
            {
              name: 'AZURE_SEARCH_ENDPOINT'
              value: 'https://${aiSearch.name}.search.windows.net'
            }
            {
              name: 'AZURE_SEARCH_API_KEY'
              secretRef: 'ai-search-key'
            }
            {
              name: 'AZURE_STORAGE_ACCOUNT_NAME'
              value: storageAccount.name
            }
            {
              name: 'KEY_VAULT_URL'
              value: keyVault.properties.vaultUri
            }
          ]
        }
      ]
      scale: {
        minReplicas: environmentName == 'prod' ? 2 : 1
        maxReplicas: environmentName == 'prod' ? 10 : 3
        rules: [
          {
            name: 'http-scaler'
            http: {
              metadata: {
                concurrentRequests: '100'
              }
            }
          }
        ]
      }
    }
  }
}

// Role Assignments
resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: containerRegistry
  name: guid(containerRegistry.id, managedIdentity.id, 'AcrPull')
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource storageContributorRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: guid(storageAccount.id, managedIdentity.id, 'StorageBlobDataContributor')
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource keyVaultSecretsRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: keyVault
  name: guid(keyVault.id, managedIdentity.id, 'KeyVaultSecretsUser')
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Outputs
output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn
output containerAppUrl string = 'https://${containerApp.properties.configuration.ingress.fqdn}'
output keyVaultName string = keyVault.name
output storageAccountName string = storageAccount.name
output postgreSQLHostname string = postgreSQL.properties.fullyQualifiedDomainName
output aiSearchEndpoint string = 'https://${aiSearch.name}.search.windows.net'
output containerRegistryLoginServer string = containerRegistry.properties.loginServer
output managedIdentityClientId string = managedIdentity.properties.clientId
output applicationInsightsConnectionString string = applicationInsights.properties.ConnectionString
