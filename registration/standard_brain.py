# set number of cores for parallelization
import os
n_core = 16;
os.environ['MKL_NUM_THREADS'] = str(16)

# specify base directory and create input and output directories
base_dir = '/groups/ahrens/ahrenslab/mika/Yu/'
os.system('mkdir -p ' + base_dir + 'template/{input,output}')

# find individual brain images
image_filenames = \
    os.popen('find ' + base_dir +
    ' -name "image_reference_aligned0.nii.gz" -not -path "*nonglia*" -not -path "*template*"')\
    .read().split('\n')

if not image_filenames[-1]:
    image_filenames.pop()

# copy individual brain images into a single folder '/template/input/'
for filename in image_filenames:
    try:
        filename.remove('ana')
    except:
        pass

    os.system('cp ' + filename + ' ' + base_dir + '/template/input/' + filename[-1] + '.nii.gz')

# antsTemplate_call
antsTemplate_call = ' '.join([
    '/groups/ahrens/home/rubinovm/ants-2.1.0-redhat/antsMultivariateTemplateConstruction2.sh',
    '-d 3',                                     # ImageDimension: 2 or 3
    '-o ' + base_dir + 'template/output/',      # OutputPrefix; prepended to all output files.
    '-i 4',                                     # Iteration limit (default 4)
    '-g 0.2',                                   # Gradient step size (default 0.25)
    '-j ' + str(n_core),                        # CPU cores (default 2; requires "-c 2")
    '-c 2',                                     # Control for parallel computation
    '-k 1',                                     # Number of modalities used for template (default 1)
    '-w 1',                                     # Modality weights in the similarity metric (default 1)
    '-f 8x4',                                   # Shrink factors (default 6x4x2x1)
    '-s 4x2',                                   # Smoothing factors (default 3x2x1x0)
    '-q 100x100',                               # Max iterations (default 100x100x70x20)
    '-n 0',                                     # N4BiasFieldCorrection of moving image: (default 1)
    '-r 1',                                     # Initial rigid-body registration of inputs (default 0)
    '-l 1',                                     # Use linear reg during deformable reg (default 1)
    '-m CC[4]',                                 # Similarity metric used for registration (default CC)
    '-t SyN[0.1,3,0]',                          # Type of transformation model for registration (default SyN)
    base_dir + '/template/input/*.nii.gz'       # List of input images
])

os.system(antsTemplate_call)
