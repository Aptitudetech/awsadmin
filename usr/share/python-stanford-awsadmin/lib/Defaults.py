# -*- python -*-

# Copyright (C) 2013, Stanford University

# EC2 classes for the RDS instance
RDS_CLASSES = [ 'db.t1.micro',
              'db.m1.small',
              'db.m1.medium',
              'db.m1.large',
              'db.m1.xlarge',
              'db.m2.xlarge',
              'db.m2.2xlarge',
              'db.m2.4xlarge',
    ]

# Default regon
RDS_REGION = 'us-west2'

# Default storage, in TB
RDS_STORAGE = '5'

# Instance prefix in instance identifier
RDS_PREFIX = 'stanford_'
