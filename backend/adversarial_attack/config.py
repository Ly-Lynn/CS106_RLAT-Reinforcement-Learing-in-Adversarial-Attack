from collections import namedtuple
import torchvision.transforms as transforms

CLASSIFIER_ARCH = "vgg16"
CLASSIFIER_TRAINED = r"C:\Users\thuyl\OneDrive - Trường ĐH CNTT - University of Information Technology\My documents\AI\ai-project\backend\adversarial_attack\Trained_model\classifier_cifar10.pth"
DATASET = "cifar10_splits"
BATCH_SIZE = 32
EPS = 20
EPSILON = 0.1
IMG_SIZE = 32 # areas: img_size ^ 2
MASK_SIZE = 4 # areas: mask_size ^ 2
NUM_MASKS = 10 

MAX_ITER = 600
NOISE_SD = 1
GAMMA = 0.9
TARGET_UPDATE = 1000

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # Assuming CIFAR-10 normalization
])

INPUT_DQN_SIZE = 580 # 512 + 64 + 4
OUTPUT_DQN_SIZE = 64
DQN_TRAINED = r"C:\Users\thuyl\OneDrive - Trường ĐH CNTT - University of Information Technology\My documents\AI\ai-project\backend\adversarial_attack\model_0.pth"
TRACK_FOLDER = "view"
TEST_FOLDER = "view_test"
ACTION_TRACK = "actions.json"
LOSS_TRACK = "losses.json"
REWARD_TRACK = "rewards.json"

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))