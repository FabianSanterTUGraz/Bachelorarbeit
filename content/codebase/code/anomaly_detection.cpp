#include <fstream>
#include <iostream>
#include <vector>

#include "include/streamingData.hpp"
#include "include/AnomalyDetection.h"
#include "include/utils.h"

void writeData(std::string filePath, std::vector<float> fileToWrite, bool append = true)
{
    std::ofstream MyFile;
    if (append)
    {
        MyFile.open(filePath, std::ios_base::app);
    }
    else
    {
        MyFile.open(filePath);
    }

    if (!MyFile.is_open())
    {
        std::cerr << "Error: Could not open or create file at path: " << filePath << std::endl;
        return;
    }

    for (std::size_t i = 0; i < fileToWrite.size(); i += 2)
    {
        MyFile << fileToWrite.at(i) << "," << fileToWrite.at(i + 1) << std::endl;
    }
    MyFile.close();
}

int main()
{
    std::vector<float> writeToFile;
    std::cout << "Real time anomaly detection...." << std::endl;
    int i = 30;
    std::string fileInput = std::to_string(i);
    std::string absolutePath = "Data/" + fileInput + ".csv";
    streamData DataStream(absolutePath);
    std::string line;

    // Time-delay embedding parameters.
    int dimensions = 6;   // number of embedding dimensions
    int tau = 20;         // delay between successive embedding coordinates
    int windowSize = 1000; // length of the sliding window buffer

    float slidingWindow[windowSize] = {0.0f}; // raw streaming values
    float tde[dimensions] = {0.0f};           // current time-delay embedding vector

    // Precompute the sliding-window offsets used to build each embedding.
    int tdeIndexes[dimensions];
    embeddingIndexes(tdeIndexes, windowSize, dimensions, tau);

    // Incrementally updated statistics for streaming PCA.
    float runningMean[dimensions] = {0.0f};
    float runningCov[dimensions * dimensions] = {0.0f};

    // Top two principal components (eigenvectors) of the embedding.
    float principalComponent1[dimensions] = {0.0f};
    float principalComponent2[dimensions] = {0.0f};

    // Initialize the components to the identity basis vectors.
    principalComponent1[0] = 1.0f;
    principalComponent2[1] = 1.0f;

    // Projection of the current embedding onto the two principal components.
    float outX = 0.0f;
    float outY = 0.0f;

    while (DataStream.hasNext())
    {
        DataStream.next(line);
        if (line.empty())
        {
            break;
        }
        float value = std::stof(line);

        if (processNewDataPoint(value, tde, slidingWindow, runningMean, runningCov, principalComponent1,
                                principalComponent2, tdeIndexes, windowSize, dimensions,
                                &outX, &outY) != 1)
        {
            writeToFile.push_back(outX);
            writeToFile.push_back(outY);
        }
    }

    std::string outputPath = "output/output.txt";
    writeData(outputPath, writeToFile, false);
    return 0;
}